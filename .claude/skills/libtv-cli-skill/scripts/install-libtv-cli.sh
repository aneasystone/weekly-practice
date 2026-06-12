#!/usr/bin/env bash
#
# LibTV CLI 一键安装：把 libtv 装到 LIBTV_CLI_INSTALL_DIR（默认 ~/.libtv），并尝试写入 shell profile 的 PATH（逻辑参考 nvm install.sh）。
# 详细环境变量与目录布局见同级目录 install.md。
#
# 本地离线包只从「脚本所在目录的上一层」下的 release/ 解析（RELEASE_DIR），不会扫仓库根 release/。
#
# 解析顺序（与 main 一致）：
#   1) LIBTV_CLI_BINARY 直接指定可执行文件
#   2) 本地 release/：优先 zip（推荐 release/<版本>/<bundle>.zip），再裸二进制 libtv
#   3) 远程：从官方静态站 liblibai-web-static 按本机平台下载（见下方 LIBTV_REMOTE_*），无需配置 URL
#
# 刻意不使用 rm 清理：远程下载的 zip、unzip 临时目录会留在系统临时目录，需自行删除（见 install.md）。
#
set -euo pipefail

# 官方远端（与 https://liblibai-web-static.liblib.cloud/cli/<ver>/libtv-<platform>.zip 一致）
LIBTV_REMOTE_BASE='https://liblibai-web-static.liblib.cloud/cli'
# latest 通道：用 latest/manifest.json 的 .version 作为远端默认版本（避免脚本里钉死版本号导致和发布脱节）
LIBTV_REMOTE_LATEST_MANIFEST_URL="${LIBTV_REMOTE_BASE}/latest/manifest.json"

# LIBTV_CLI_VERSION：定向把安装/更新钉到某个版本
#   - 远端：下载 URL 变成 ${LIBTV_REMOTE_BASE}/${LIBTV_CLI_VERSION}/<bundle>.zip
#   - 本地：resolve_local_release_* 只看 release/${LIBTV_CLI_VERSION}/，不再回退到其它版本
# 未设置则远端去拉 latest/manifest.json 取 .version；本地仍挑最高版本
LIBTV_VERSION_PIN="${LIBTV_CLI_VERSION:-}"

die() { echo "error: $*" >&2; exit 1; } # 非零退出；set -e 下用于显式失败

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RELEASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)/release"
INSTALL_DIR="${LIBTV_CLI_INSTALL_DIR:-$HOME/.libtv}"

# ---------------------------------------------------------------------------
# shell profile：检测 ~/.zshrc 等，追加 PATH（与 nvm 的 nvm_detect_profile / 写 profile 思路一致）
# ---------------------------------------------------------------------------

# 若存在且为普通文件则 stdout 打印路径
libtv_try_profile() {
  [[ -n "${1:-}" && -f "$1" ]] && { echo "$1"; return 0; }
  return 1
}

# 输出一个可写入的 profile 路径；无则返回 1。支持 LIBTV_CLI_PROFILE / PROFILE 覆盖；PROFILE=/dev/null 表示不写
libtv_detect_profile() {
  if [[ "${LIBTV_CLI_PROFILE:-}" == '/dev/null' ]] || [[ "${PROFILE:-}" == '/dev/null' ]]; then
    return 1
  fi
  if [[ -n "${LIBTV_CLI_PROFILE:-}" ]] && libtv_try_profile "$LIBTV_CLI_PROFILE"; then return 0; fi
  if [[ -n "${PROFILE:-}" ]] && libtv_try_profile "$PROFILE"; then return 0; fi

  local DETECTED p zd
  DETECTED=''
  zd="${ZDOTDIR:-$HOME}"
  if [[ "${SHELL:-}" == *bash* ]]; then
    DETECTED="$(libtv_try_profile "$HOME/.bashrc" || true)"
    [[ -z "$DETECTED" ]] && DETECTED="$(libtv_try_profile "$HOME/.bash_profile" || true)"
  elif [[ "${SHELL:-}" == *zsh* ]]; then
    DETECTED="$(libtv_try_profile "$zd/.zshrc" || true)"
    [[ -z "$DETECTED" ]] && DETECTED="$(libtv_try_profile "$zd/.zprofile" || true)"
  fi
  if [[ -z "$DETECTED" ]]; then
    for p in ".profile" ".bashrc" ".bash_profile" ".zprofile" ".zshrc"; do
      DETECTED="$(libtv_try_profile "$zd/$p" || true)"
      [[ -n "$DETECTED" ]] && break
    done
  fi
  [[ -n "$DETECTED" ]] && { echo "$DETECTED"; return 0; }
  return 1
}

# 安装目录绝对路径写入 profile，export PATH="<dir>:$PATH"；已存在标记行则跳过
libtv_append_path_to_profile() {
  local install_abs="$1"
  local marker='# libtv-cli: PATH (install-libtv-cli.sh)'
  local prof

  if [[ "${LIBTV_CLI_SKIP_PROFILE:-}" == 1 ]]; then
    libtv_print_path_hint "$install_abs"
    return 0
  fi
  if [[ "${LIBTV_CLI_PROFILE:-}" == '/dev/null' ]] || [[ "${PROFILE:-}" == '/dev/null' ]]; then
    libtv_print_path_hint "$install_abs"
    return 0
  fi

  if ! prof="$(libtv_detect_profile)"; then
    echo "=> Profile not found. Append the following to your shell rc file, then restart the terminal:" >&2
    printf '%s\n' "$marker" "export PATH=\"${install_abs}:\$PATH\"" >&2
    return 0
  fi

  if grep -qF "$marker" "$prof" 2>/dev/null; then
    echo "=> libtv PATH line already present in $prof" >&2
    libtv_print_path_hint "$install_abs"
    return 0
  fi

  echo "=> Appending libtv PATH to $prof" >&2
  {
    printf '\n%s\n' "$marker"
    echo "export PATH=\"${install_abs}:\$PATH\""
  } >>"$prof" || die "cannot append to profile: $prof"
  echo "=> Close and reopen your terminal, or run:  source \"${prof}\"" >&2
  libtv_print_path_hint "$install_abs"
}

# 若当前进程 PATH 尚未包含安装目录，提示一行（新开终端后一般不再需要）
libtv_print_path_hint() {
  local install_abs="$1"
  if [[ ":${PATH}:" != *":${install_abs}:"* ]]; then
    echo "当前 shell 的 PATH 尚未包含: $install_abs" >&2
    echo "执行:  export PATH=\"${install_abs}:\$PATH\"  或重开终端后再试 libtv" >&2
  fi
}

# ---------------------------------------------------------------------------
# 平台识别：uname → OS / arch / slug（如 darwin-arm64）/ 发布用 bundle 目录名
# ---------------------------------------------------------------------------

detect_os() {
  case "$(uname -s)" in
    Darwin) echo darwin ;;
    Linux) echo linux ;;
    *) die "unsupported OS: $(uname -s) (expected Darwin or Linux)" ;;
  esac
}

detect_arch() {
  case "$(uname -m)" in
    x86_64|amd64) echo amd64 ;;
    arm64|aarch64) echo arm64 ;;
    *) die "unsupported arch: $(uname -m) (expected x86_64/amd64 or arm64/aarch64)" ;;
  esac
}

platform_slug() {
  echo "$(detect_os)-$(detect_arch)"
}

# 与产物命名一致：release/<版本>/libtv-macos-arm64.zip 里的 libtv-macos-arm64 等
bundle_dir_name() {
  local os arch
  os="$(detect_os)"
  arch="$(detect_arch)"
  case "$os-$arch" in
    darwin-arm64) echo libtv-macos-arm64 ;;
    darwin-amd64) echo libtv-macos-x64 ;;
    linux-arm64) echo libtv-linux-arm64 ;;
    linux-amd64) echo libtv-linux-x64 ;;
    *) die "unsupported bundle for $os-$arch" ;;
  esac
}

# 仅 v1.2.3 / 1.2.3 形态算作「版本目录」；darwin-arm64 等平铺目录不参与版本排序
is_version_dir_name() {
  [[ "$1" =~ ^(v[0-9]+|[0-9]+)(\.[0-9]+)*$ ]]
}

# 在各版本子目录中按语义版本从高到低找：…/<ver>/<bundle>/libtv
find_highest_versioned_bundle_binary() {
  local bundle="$1" release_dir="$2"
  local d bn ver p
  local -a names=()
  [[ -d "$release_dir" ]] || return 1
  while IFS= read -r -d '' d; do
    bn="$(basename "$d")"
    is_version_dir_name "$bn" || continue
    names+=("$bn")
  done < <(find "$release_dir" -maxdepth 1 -mindepth 1 -type d -print0 2>/dev/null)
  [[ ${#names[@]} -eq 0 ]] && return 1
  while IFS= read -r ver; do
    [[ -z "$ver" ]] && continue
    p="$release_dir/$ver/$bundle/libtv"
    [[ -f "$p" ]] && { echo "$p"; return 0; }
  done < <(printf '%s\n' "${names[@]}" | LC_ALL=C sort -V -r)
  return 1
}

# 历史布局：…/<ver>/<bundle>/libtv.zip（bundle 为子目录）
find_highest_versioned_bundle_libtv_zip() {
  local bundle="$1" release_dir="$2"
  local d bn ver p
  local -a names=()
  [[ -d "$release_dir" ]] || return 1
  while IFS= read -r -d '' d; do
    bn="$(basename "$d")"
    is_version_dir_name "$bn" || continue
    names+=("$bn")
  done < <(find "$release_dir" -maxdepth 1 -mindepth 1 -type d -print0 2>/dev/null)
  [[ ${#names[@]} -eq 0 ]] && return 1
  while IFS= read -r ver; do
    [[ -z "$ver" ]] && continue
    p="$release_dir/$ver/$bundle/libtv.zip"
    [[ -f "$p" ]] && { echo "$p"; return 0; }
  done < <(printf '%s\n' "${names[@]}" | LC_ALL=C sort -V -r)
  return 1
}

# 仅在指定版本目录中查 zip：…/<ver>/<zip_name> 与 …/<ver>/<bundle>/<zip_name>
find_pinned_version_release_zip_at() {
  local zip_name="$1" bundle="$2" release_dir="$3" ver="$4" p
  [[ -n "$ver" && -d "$release_dir/$ver" ]] || return 1
  p="$release_dir/$ver/$zip_name"
  [[ -f "$p" ]] && { echo "$p"; return 0; }
  p="$release_dir/$ver/$bundle/$zip_name"
  [[ -f "$p" ]] && { echo "$p"; return 0; }
  return 1
}

# 仅在指定版本目录中查 …/<ver>/<bundle>/libtv.zip
find_pinned_version_bundle_libtv_zip() {
  local bundle="$1" release_dir="$2" ver="$3" p
  [[ -n "$ver" && -d "$release_dir/$ver" ]] || return 1
  p="$release_dir/$ver/$bundle/libtv.zip"
  [[ -f "$p" ]] && { echo "$p"; return 0; }
  return 1
}

# 仅在指定版本目录中查 …/<ver>/<bundle>/libtv（裸二进制）
find_pinned_version_bundle_binary() {
  local bundle="$1" release_dir="$2" ver="$3" p
  [[ -n "$ver" && -d "$release_dir/$ver" ]] || return 1
  p="$release_dir/$ver/$bundle/libtv"
  [[ -f "$p" ]] && { echo "$p"; return 0; }
  return 1
}

# 在各版本子目录中从高到低试：…/<ver>/<zip_name> 与 …/<ver>/<bundle>/<zip_name>
find_highest_versioned_release_zip_at() {
  local zip_name="$1" bundle="$2" release_dir="$3"
  local d bn ver p
  local -a names=()
  [[ -d "$release_dir" ]] || return 1
  while IFS= read -r -d '' d; do
    bn="$(basename "$d")"
    is_version_dir_name "$bn" || continue
    names+=("$bn")
  done < <(find "$release_dir" -maxdepth 1 -mindepth 1 -type d -print0 2>/dev/null)
  [[ ${#names[@]} -eq 0 ]] && return 1
  while IFS= read -r ver; do
    [[ -z "$ver" ]] && continue
    p="$release_dir/$ver/$zip_name"
    [[ -f "$p" ]] && { echo "$p"; return 0; }
    p="$release_dir/$ver/$bundle/$zip_name"
    [[ -f "$p" ]] && { echo "$p"; return 0; }
  done < <(printf '%s\n' "${names[@]}" | LC_ALL=C sort -V -r)
  return 1
}

# 与官方远端 / 推荐本地 release 一致：libtv-macos-arm64.zip 等
zip_basename() {
  echo "$(bundle_dir_name).zip"
}

# 每行一个候选 zip 文件名：先官方 bundle 名，再历史 libtv-darwin-*.zip
local_zip_candidate_names() {
  local primary os arch
  primary="$(zip_basename)"
  echo "$primary"
  os="$(detect_os)"; arch="$(detect_arch)"
  if [[ "libtv-${os}-${arch}.zip" != "$primary" ]]; then
    echo "libtv-${os}-${arch}.zip"
  fi
}

ZIP_NAME="$(zip_basename)"

fetch_url() {
  # 下载到已有路径（由调用方 mktemp）；优先 curl，其次 wget
  local url="$1" out="$2"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL --connect-timeout 30 --retry 2 -o "$out" "$url"
  elif command -v wget >/dev/null 2>&1; then
    wget -q -O "$out" "$url"
  else
    die "need curl or wget to download"
  fi
}

# ---------------------------------------------------------------------------
# 本地 release/：在 RELEASE_DIR 下找裸二进制 libtv（无 zip 时的回退）
# ---------------------------------------------------------------------------

resolve_local_release_binary() {
  local bundle slug p
  bundle="$(bundle_dir_name)"
  slug="$(platform_slug)"
  [[ -d "$RELEASE_DIR" ]] || return 1
  # 指定了 LIBTV_CLI_VERSION 时仅看该版本目录，不回退到更低版本或平铺布局
  if [[ -n "$LIBTV_VERSION_PIN" ]]; then
    find_pinned_version_bundle_binary "$bundle" "$RELEASE_DIR" "$LIBTV_VERSION_PIN"
    return $?
  fi
  if p="$(find_highest_versioned_bundle_binary "$bundle" "$RELEASE_DIR")"; then
    echo "$p"
    return 0
  fi
  p="$RELEASE_DIR/$slug/libtv"
  [[ -f "$p" ]] && { echo "$p"; return 0; }
  p="$RELEASE_DIR/libtv"
  [[ -f "$p" ]] && { echo "$p"; return 0; }
  return 1
}

# 本地 release/：按优先级找 zip（成功则 stdout 打印绝对路径）
resolve_local_release_zip() {
  local bundle slug p zip_name
  bundle="$(bundle_dir_name)"
  slug="$(platform_slug)"
  [[ -d "$RELEASE_DIR" ]] || return 1
  # 指定了 LIBTV_CLI_VERSION 时仅查找该版本目录下的包，不回退到其它版本或平铺布局
  if [[ -n "$LIBTV_VERSION_PIN" ]]; then
    if p="$(find_pinned_version_release_zip_at "${bundle}.zip" "$bundle" "$RELEASE_DIR" "$LIBTV_VERSION_PIN")"; then
      echo "$p"; return 0
    fi
    if p="$(find_pinned_version_bundle_libtv_zip "$bundle" "$RELEASE_DIR" "$LIBTV_VERSION_PIN")"; then
      echo "$p"; return 0
    fi
    while IFS= read -r zip_name; do
      [[ -z "$zip_name" ]] && continue
      [[ "$zip_name" == "${bundle}.zip" ]] && continue
      if p="$(find_pinned_version_release_zip_at "$zip_name" "$bundle" "$RELEASE_DIR" "$LIBTV_VERSION_PIN")"; then
        echo "$p"; return 0
      fi
    done < <(local_zip_candidate_names)
    return 1
  fi
  # 推荐：release/<版本>/<bundle>.zip（如 release/0.0.9/libtv-macos-arm64.zip）
  if p="$(find_highest_versioned_release_zip_at "${bundle}.zip" "$bundle" "$RELEASE_DIR")"; then
    echo "$p"
    return 0
  fi
  if p="$(find_highest_versioned_bundle_libtv_zip "$bundle" "$RELEASE_DIR")"; then
    echo "$p"
    return 0
  fi
  p="$RELEASE_DIR/$slug/libtv.zip"
  [[ -f "$p" ]] && { echo "$p"; return 0; }
  p="$RELEASE_DIR/libtv.zip"
  [[ -f "$p" ]] && { echo "$p"; return 0; }
  while IFS= read -r zip_name; do
    [[ -z "$zip_name" ]] && continue
    # ${bundle}.zip 已在上面优先匹配
    [[ "$zip_name" == "${bundle}.zip" ]] && continue
    if p="$(find_highest_versioned_release_zip_at "$zip_name" "$bundle" "$RELEASE_DIR")"; then
      echo "$p"
      return 0
    fi
    p="$RELEASE_DIR/$slug/$zip_name"
    [[ -f "$p" ]] && { echo "$p"; return 0; }
    p="$RELEASE_DIR/$zip_name"
    [[ -f "$p" ]] && { echo "$p"; return 0; }
  done < <(local_zip_candidate_names)
  return 1
}

# ---------------------------------------------------------------------------
# 远程 zip：liblib 静态站；失败时打印 install hint 后 die
# ---------------------------------------------------------------------------

# 拉 latest/manifest.json 取 .version；用 grep/sed 解析，避免 jq 依赖。
# 失败仅写 stderr 并返回非 0，由调用方负责 die（避免在命令替换中 exit 被吞掉）。
resolve_latest_remote_version() {
  local tmp ver
  tmp="$(mktemp -t libtv_cli_manifest.XXXXXX)"
  echo "正在解析最新版本: $LIBTV_REMOTE_LATEST_MANIFEST_URL" >&2
  if ! fetch_url "$LIBTV_REMOTE_LATEST_MANIFEST_URL" "$tmp"; then
    echo "error: 无法获取 latest manifest（$LIBTV_REMOTE_LATEST_MANIFEST_URL）" >&2
    return 1
  fi
  ver="$(grep -oE '"version"[[:space:]]*:[[:space:]]*"[^"]+"' "$tmp" | head -n1 | sed -E 's/.*"([^"]+)"[[:space:]]*$/\1/')"
  if [[ -z "$ver" ]]; then
    echo "error: latest manifest 缺少 version 字段（$LIBTV_REMOTE_LATEST_MANIFEST_URL）" >&2
    return 1
  fi
  echo "$ver"
}

resolve_remote_zip() {
  local tmp url ver
  if [[ -n "$LIBTV_VERSION_PIN" ]]; then
    ver="$LIBTV_VERSION_PIN"
  else
    # 命令替换吞 exit，需显式检查返回码（macOS Bash 3.2 无 inherit_errexit）
    ver="$(resolve_latest_remote_version)" || die "无法解析远端默认版本；可改用 LIBTV_CLI_VERSION=<版本> 指定版本"
    [[ -n "$ver" ]] || die "无法解析远端默认版本；可改用 LIBTV_CLI_VERSION=<版本> 指定版本"
  fi
  url="${LIBTV_REMOTE_BASE}/${ver}/$(bundle_dir_name).zip"
  tmp="$(mktemp -t libtv_cli_zip.XXXXXX)"
  echo "正在下载: $url" >&2
  fetch_url "$url" "$tmp" || {
    local bundle slug
    bundle="$(bundle_dir_name)"
    slug="$(platform_slug)"
    print_install_source_hint "$bundle" "$slug" "$ZIP_NAME"
    local pin_hint=''
    [[ -n "$LIBTV_VERSION_PIN" ]] && pin_hint="
已通过 LIBTV_CLI_VERSION=${LIBTV_VERSION_PIN} 定向到该版本；远端仅尝试该版本的 URL。确认服务端存在该版本，或改用其它版本/取消该变量。"
    die "no libtv found. 远程下载失败: $url${pin_hint}
本地目录（脚本上一级/release/）: ${RELEASE_DIR}
zip（推荐）: <版本>/${bundle}.zip；亦支持 <版本>/${bundle}/libtv.zip 等
仍支持裸二进制: <版本>/${bundle}/libtv、${slug}/libtv、libtv"
  }
  echo "$tmp"
}

# 本地解析失败时写 stderr：目录是否为空、是否与仓库根 release/ 混淆等
print_install_source_hint() {
  local bundle="$1" slug="$2" zipn="$3" repo_rel f
  echo "" >&2
  echo "---- why install failed (local) ----" >&2
  echo "only searches: ${RELEASE_DIR}" >&2
  if [[ ! -d "$RELEASE_DIR" ]]; then
    echo "this path is not a directory; create it: mkdir -p \"${RELEASE_DIR}\"" >&2
  elif [[ -z "$(find "$RELEASE_DIR" -mindepth 1 -print -quit 2>/dev/null)" ]]; then
    echo "this directory is empty — put a platform zip or bare libtv here (see install.md)." >&2
    echo "example: ${RELEASE_DIR}/0.0.9/${bundle}.zip" >&2
    case "$RELEASE_DIR" in
      */.cursor/skills/libtv-cli/release)
        repo_rel="$(cd "$SCRIPT_DIR/../../../.." && pwd)/release"
        if [[ -d "$repo_rel" && "$repo_rel" != "$RELEASE_DIR" ]]; then
          echo "repo release (not used by this script): ${repo_rel}" >&2
          while IFS= read -r f; do echo "  - $(basename "$f")" >&2; done < <(find "$repo_rel" -maxdepth 1 -type f 2>/dev/null | LC_ALL=C sort)
          echo "note: libtv-cli-skill.zip is the whole skill bundle, not a per-platform CLI zip with libtv inside." >&2
          echo "      copy your signed libtv.zip or ${zipn} into: ${RELEASE_DIR}/" >&2
        fi
        ;;
    esac
  else
    echo "directory is not empty but nothing matched this machine (${bundle} / ${zipn}); sample files:" >&2
    find "$RELEASE_DIR" -mindepth 1 -maxdepth 4 -type f 2>/dev/null | head -20 | sed 's/^/  /' >&2
  fi
}

# ---------------------------------------------------------------------------
# 安装：依赖检查、复制二进制、从 zip 解压后安装
# ---------------------------------------------------------------------------

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "missing command: $1"
}

install_copy_binary() {
  # 统一安装到 INSTALL_DIR/libtv；cp -f 会覆盖已有同名文件
  local binary_src="$1" dest install_abs
  mkdir -p "$INSTALL_DIR"
  dest="$INSTALL_DIR/libtv"
  cp -f "$binary_src" "$dest"
  chmod +x "$dest"
  install_abs="$(cd "$INSTALL_DIR" && pwd)"
  echo "Installed: $dest"
  libtv_append_path_to_profile "$install_abs"
  "$dest" --help >/dev/null 2>&1 || true
}

install_from_zip_path() {
  # 解压到 mktemp 目录（脚本不 rm，目录会留在 $TMPDIR）；包内任一层找 libtv / libtv.exe
  local zip_path="$1" extract_dir binary_src
  [[ -f "$zip_path" ]] || die "not a zip file: $zip_path"
  need_cmd unzip
  extract_dir="$(mktemp -d -t libtv_cli_extract.XXXXXX)"
  unzip -q -o "$zip_path" -d "$extract_dir"
  binary_src="$(find "$extract_dir" \( -name libtv -o -name libtv.exe \) -type f | head -n 1)"
  [[ -n "$binary_src" ]] || die "no libtv binary found inside zip: $zip_path (expected libtv or libtv.exe)"
  install_copy_binary "$binary_src"
}

main() {
  local binary_src zip_path

  # 与文件头「解析顺序」一致
  if [[ -n "${LIBTV_CLI_BINARY:-}" ]]; then
    [[ -f "$LIBTV_CLI_BINARY" ]] || die "LIBTV_CLI_BINARY is not a file: $LIBTV_CLI_BINARY"
    install_copy_binary "$LIBTV_CLI_BINARY"
    return
  fi

  if zip_path="$(resolve_local_release_zip)"; then
    install_from_zip_path "$zip_path"
    return
  fi

  if binary_src="$(resolve_local_release_binary)"; then
    install_copy_binary "$binary_src"
    return
  fi

  # 本地皆失败：从官方站下载；失败时 resolve_remote_zip 会 die
  zip_path="$(resolve_remote_zip)"
  install_from_zip_path "$zip_path"
}

main "$@" # 入口
