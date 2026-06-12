# LibTV CLI installer. See install.md in the same directory.
# Usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File install-libtv-cli.ps1
#   Invoke-WebRequest https://liblibai-web-static.liblib.cloud/cli/latest/install-libtv-cli.ps1 -UseBasicParsing | Invoke-Expression

$ErrorActionPreference = 'Stop'

# Keep the URL shape aligned with macOS/Linux:
# https://liblibai-web-static.liblib.cloud/cli/<version>/libtv-<platform>.zip
$LibtvRemoteBase = 'https://liblibai-web-static.liblib.cloud/cli'
# latest channel: resolve the default remote version from latest/manifest.json.
$LibtvRemoteLatestManifestUrl = "$LibtvRemoteBase/latest/manifest.json"

# LIBTV_CLI_VERSION pins install/update to one version.
#   - Remote: download URL becomes $LibtvRemoteBase/<version>/libtv-windows-<arch>.zip
#   - Local: Resolve-LocalReleaseBinary only checks release\<version>\
# When unset, remote install reads latest/manifest.json; local install uses the highest version.
$LibtvVersionPin = if ($env:LIBTV_CLI_VERSION) { $env:LIBTV_CLI_VERSION } else { '' }

function Die([string]$Msg) {
    Write-Error $Msg
    exit 1
}

$ScriptPath = if ($PSCommandPath) { $PSCommandPath } elseif ($MyInvocation.MyCommand.Path) { $MyInvocation.MyCommand.Path } else { '' }
$ScriptDir = if ($ScriptPath) { Split-Path -Parent $ScriptPath } else { '' }
# Match install-libtv-cli.sh: only use release/ under the parent of this script directory.
# When executed through Invoke-WebRequest ... | Invoke-Expression there is no script path, so skip local release probing.
$ReleaseDir = ''
if ($ScriptDir) {
    $releaseParent = Resolve-Path -LiteralPath (Join-Path $ScriptDir '..') -ErrorAction SilentlyContinue
    if ($releaseParent) {
        $ReleaseDir = Join-Path $releaseParent.Path 'release'
    }
}
$DefaultInstall = Join-Path $env:USERPROFILE '.libtv'
$InstallDir = if ($env:LIBTV_CLI_INSTALL_DIR) { $env:LIBTV_CLI_INSTALL_DIR } else { $DefaultInstall }

# Remote zip temp file, removed in finally.
$script:_LibtvDownloadedZip = $null

$Arch = 'amd64'
if ($env:PROCESSOR_ARCHITECTURE -eq 'ARM64') { $Arch = 'arm64' }
$PlatformSlug = "windows-$Arch"
$ZipName = "libtv-windows-$Arch.zip"

$BundleDirName = if ($Arch -eq 'arm64') { 'libtv-win-arm64' } else { 'libtv-win-x64' }

function Parse-ReleaseDirVersion([string]$Name) {
    if ($Name -notmatch '^(v[0-9]+|[0-9]+)(\.[0-9]+)*$') { return $null }
    $s = $Name.TrimStart('v')
    if ($s -match '^\d+$') { $s = "$s.0" }
    try { return [version]$s } catch { return $null }
}

function Find-HighestVersionedBundleExe {
    param([string]$Root, [string]$Bundle)
    if (-not $Root -or -not (Test-Path -LiteralPath $Root)) { return $null }
    $rows = @(Get-ChildItem -LiteralPath $Root -Directory -ErrorAction SilentlyContinue | ForEach-Object {
            $ver = Parse-ReleaseDirVersion $_.Name
            if ($null -eq $ver) { return }
            [pscustomobject]@{ FullName = $_.FullName; Ver = $ver }
        }) | Sort-Object Ver -Descending
    foreach ($row in $rows) {
        $p = Join-Path (Join-Path $row.FullName $Bundle) 'libtv.exe'
        if (Test-Path -LiteralPath $p -PathType Leaf) {
            return (Resolve-Path $p).Path
        }
    }
    return $null
}

# Only check release\<version>\<bundle>\libtv.exe.
function Find-PinnedVersionBundleExe {
    param([string]$Root, [string]$Bundle, [string]$Version)
    if (-not $Version) { return $null }
    $verDir = Join-Path $Root $Version
    if (-not (Test-Path -LiteralPath $verDir -PathType Container)) { return $null }
    $p = Join-Path $verDir (Join-Path $Bundle 'libtv.exe')
    if (Test-Path -LiteralPath $p -PathType Leaf) {
        return (Resolve-Path $p).Path
    }
    return $null
}

# Local zip candidates: prefer official remote names, then bundle directory names.
function Get-LocalZipCandidateNames {
    $primary = $ZipName
    $alt = "$BundleDirName.zip"
    if ($alt -ne $primary) {
        return @($primary, $alt)
    }
    return @($primary)
}

# Search release\<version>\ and release\<version>\<bundle>\ for <zipName>.
function Find-VersionedReleaseZip {
    param([string]$Root, [string]$Bundle, [string]$Version, [string]$ZipFile)
    if (-not $Root) { return $null }
    $verDir = Join-Path $Root $Version
    if (-not (Test-Path -LiteralPath $verDir -PathType Container)) { return $null }
    $p = Join-Path $verDir $ZipFile
    if (Test-Path -LiteralPath $p -PathType Leaf) { return (Resolve-Path $p).Path }
    $p = Join-Path $verDir (Join-Path $Bundle $ZipFile)
    if (Test-Path -LiteralPath $p -PathType Leaf) { return (Resolve-Path $p).Path }
    return $null
}

# Search all version directories, highest version first.
function Find-HighestVersionedReleaseZip {
    param([string]$Root, [string]$Bundle, [string]$ZipFile)
    if (-not $Root -or -not (Test-Path -LiteralPath $Root)) { return $null }
    $rows = @(Get-ChildItem -LiteralPath $Root -Directory -ErrorAction SilentlyContinue | ForEach-Object {
            $ver = Parse-ReleaseDirVersion $_.Name
            if ($null -eq $ver) { return }
            [pscustomobject]@{ Name = $_.Name; Ver = $ver }
        }) | Sort-Object Ver -Descending
    foreach ($row in $rows) {
        $p = Find-VersionedReleaseZip -Root $Root -Bundle $Bundle -Version $row.Name -ZipFile $ZipFile
        if ($p) { return $p }
    }
    return $null
}

function Resolve-LocalReleaseZip {
    if (-not $ReleaseDir -or -not (Test-Path -LiteralPath $ReleaseDir -PathType Container)) { return $null }
    $candidates = Get-LocalZipCandidateNames

    # With LIBTV_CLI_VERSION, only check that version directory.
    if ($LibtvVersionPin) {
        foreach ($zip in $candidates) {
            $p = Find-VersionedReleaseZip -Root $ReleaseDir -Bundle $BundleDirName -Version $LibtvVersionPin -ZipFile $zip
            if ($p) { return $p }
        }
        return $null
    }

    foreach ($zip in $candidates) {
        $p = Find-HighestVersionedReleaseZip -Root $ReleaseDir -Bundle $BundleDirName -ZipFile $zip
        if ($p) { return $p }
        # Flat-layout fallback: release\<slug>\<zip> and release\<zip>.
        $p = Join-Path $ReleaseDir (Join-Path $PlatformSlug $zip)
        if (Test-Path -LiteralPath $p -PathType Leaf) { return (Resolve-Path $p).Path }
        $p = Join-Path $ReleaseDir $zip
        if (Test-Path -LiteralPath $p -PathType Leaf) { return (Resolve-Path $p).Path }
    }
    return $null
}

function Download-Url([string]$Url, [string]$OutFile) {
    Invoke-WebRequest -Uri $Url -OutFile $OutFile -UseBasicParsing
}

function Resolve-LocalReleaseBinary {
    if (-not $ReleaseDir) { return $null }
    # With LIBTV_CLI_VERSION, do not fall back to other versions or flat layouts.
    if ($LibtvVersionPin) {
        return (Find-PinnedVersionBundleExe -Root $ReleaseDir -Bundle $BundleDirName -Version $LibtvVersionPin)
    }
    $p = Find-HighestVersionedBundleExe -Root $ReleaseDir -Bundle $BundleDirName
    if ($p) { return $p }
    $legacy = Join-Path (Join-Path $ReleaseDir $PlatformSlug) 'libtv.exe'
    if (Test-Path -LiteralPath $legacy -PathType Leaf) {
        return (Resolve-Path $legacy).Path
    }
    $p2 = Join-Path $ReleaseDir 'libtv.exe'
    if (Test-Path -LiteralPath $p2 -PathType Leaf) {
        return (Resolve-Path $p2).Path
    }
    return $null
}

function Resolve-LatestRemoteVersion {
    # Read .version from latest/manifest.json. Invoke-RestMethod parses JSON.
    Write-Host "Resolving latest version: $LibtvRemoteLatestManifestUrl"
    try {
        $resp = Invoke-RestMethod -Uri $LibtvRemoteLatestManifestUrl -UseBasicParsing
    }
    catch {
        Die "Failed to fetch latest manifest ($LibtvRemoteLatestManifestUrl): $($_.Exception.Message). You can set LIBTV_CLI_VERSION=<version>."
    }
    $ver = if ($resp -and $resp.version) { [string]$resp.version } else { '' }
    if (-not $ver) {
        Die "latest manifest is missing the version field ($LibtvRemoteLatestManifestUrl)."
    }
    return $ver
}

function Resolve-RemoteZip {
    $ver = if ($LibtvVersionPin) { $LibtvVersionPin } else { Resolve-LatestRemoteVersion }
    $url = ("{0}/{1}/{2}" -f $LibtvRemoteBase.TrimEnd('/'), $ver, $ZipName)
    $tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("libtv_cli_" + [Guid]::NewGuid().ToString('N') + '.zip')
    $script:_LibtvDownloadedZip = $tmp
    Write-Host "Downloading: $url"
    try {
        Download-Url $url $tmp
    }
    catch {
        $script:_LibtvDownloadedZip = $null
        if (Test-Path -LiteralPath $tmp) {
            Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
        }
        $pinHint = ''
        if ($LibtvVersionPin) {
            $pinHint = "`nLIBTV_CLI_VERSION=$LibtvVersionPin is set, so only that remote version was tried. Confirm the version exists, set another version, or unset LIBTV_CLI_VERSION."
        }
        Die @"
no libtv found. Remote download failed: $url$pinHint
Local preferred layout: release\<highest-version>\$BundleDirName\libtv.exe, for example release\0.0.9\$BundleDirName\libtv.exe
Legacy layouts: release\$PlatformSlug\libtv.exe or release\libtv.exe
"@
    }
    return $tmp
}

function Install-Binary([string]$SourcePath) {
    if (-not (Test-Path $InstallDir)) {
        New-Item -ItemType Directory -Path $InstallDir | Out-Null
    }
    $dest = Join-Path $InstallDir 'libtv.exe'
    Copy-Item -LiteralPath $SourcePath -Destination $dest -Force
    Write-Host "Installed: $dest"
    if ($env:LIBTV_CLI_SKIP_PROFILE -eq '1' -or $env:LIBTV_CLI_PROFILE -eq '/dev/null' -or $env:PROFILE -eq '/dev/null') {
        Write-Host "Skipping user PATH update (LIBTV_CLI_SKIP_PROFILE or profile=/dev/null). Add manually: $InstallDir" -ForegroundColor Yellow
        return
    }
    $machinePath = [Environment]::GetEnvironmentVariable('Path', 'User')
    if ($null -eq $machinePath) { $machinePath = '' }
    # Split on ';' and compare whole entries case-insensitively.
    $entries = $machinePath.Split(';') | Where-Object { $_ -ne '' }
    $already = $false
    foreach ($e in $entries) {
        if ([string]::Equals($e.TrimEnd([char]92), $InstallDir.TrimEnd([char]92), [System.StringComparison]::OrdinalIgnoreCase)) {
            $already = $true
            break
        }
    }
    if (-not $already) {
        $newPath = if ($machinePath) { "${InstallDir};${machinePath}" } else { $InstallDir }
        [Environment]::SetEnvironmentVariable('Path', $newPath, 'User')
        Write-Host "Added to user PATH: $InstallDir"
    }
    else {
        Write-Host "User PATH already contains: $InstallDir"
    }
    # Make the current session usable too; SetEnvironmentVariable does not update this process.
    $sessionEntries = $env:Path.Split(';') | Where-Object { $_ -ne '' }
    $inSession = $false
    foreach ($e in $sessionEntries) {
        if ([string]::Equals($e.TrimEnd([char]92), $InstallDir.TrimEnd([char]92), [System.StringComparison]::OrdinalIgnoreCase)) {
            $inSession = $true
            break
        }
    }
    if (-not $inSession) {
        $env:Path = "${InstallDir};$env:Path"
        Write-Host "Current session PATH updated: $InstallDir. New terminals will include it automatically."
    }
}

if ($env:LIBTV_CLI_BINARY) {
    if (-not (Test-Path -LiteralPath $env:LIBTV_CLI_BINARY -PathType Leaf)) {
        Die "LIBTV_CLI_BINARY is not a file: $($env:LIBTV_CLI_BINARY)"
    }
    Install-Binary (Resolve-Path $env:LIBTV_CLI_BINARY).Path
    return
}

function Install-FromZip([string]$ZipPath) {
    $extractRoot = Join-Path $env:TEMP ('libtv_cli_extract_' + [Guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $extractRoot | Out-Null
    try {
        Expand-Archive -LiteralPath $ZipPath -DestinationPath $extractRoot -Force
        $binary = Get-ChildItem -Path $extractRoot -Recurse -File -Filter 'libtv.exe' -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if (-not $binary) {
            $binary = Get-ChildItem -Path $extractRoot -Recurse -File -Filter 'libtv' -ErrorAction SilentlyContinue |
                Select-Object -First 1
        }
        if (-not $binary) {
            Die "no libtv.exe or libtv binary found inside zip: $ZipPath"
        }
        Install-Binary $binary.FullName
    }
    finally {
        Remove-Item -LiteralPath $extractRoot -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# Resolution order, matching install-libtv-cli.sh: local zip, local binary, remote zip.
$localZip = Resolve-LocalReleaseZip
if ($localZip) {
    Install-FromZip $localZip
    return
}

$localBin = Resolve-LocalReleaseBinary
if ($localBin) {
    Install-Binary $localBin
    return
}

try {
    $zipPath = Resolve-RemoteZip
    Install-FromZip $zipPath
}
finally {
    if ($script:_LibtvDownloadedZip -and (Test-Path -LiteralPath $script:_LibtvDownloadedZip)) {
        Remove-Item -LiteralPath $script:_LibtvDownloadedZip -Force -ErrorAction SilentlyContinue
    }
}
