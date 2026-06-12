# 一键安装 LibTV CLI（`libtv`）

**一键安装**脚本从官方静态站按本机平台下载对应的 zip，解压后把可执行文件安装到 **`LIBTV_CLI_INSTALL_DIR`**（默认 **`~/.libtv`**）下的 **`libtv`**（Windows 为 **`libtv.exe`**）。

**一键安装**脚本路径：**`scripts/install-libtv-cli.sh`**（macOS / Linux）、**`scripts/install-libtv-cli.ps1`** 与 **`scripts/install-libtv-cli.bat`**（Windows）。

---

## 远端 zip（按平台分包）

脚本会按以下规则拼出下载 URL 并拉取：

**`https://liblibai-web-static.liblib.cloud/cli/<version>/<zip>`**

其中 **`<version>`** 默认通过 **`https://liblibai-web-static.liblib.cloud/cli/latest/manifest.json`** 的 **`.version`** 字段动态解析（脚本不再内置默认版本号，避免和发布脱节）；设了 **`LIBTV_CLI_VERSION`** 时直接用它、不再去取 latest manifest（见下方「安装指定版本」）。**`<zip>`** 按本机平台取：

| 平台                | 文件名                    |
| ------------------- | ------------------------- |
| macOS Apple Silicon | `libtv-macos-arm64.zip`   |
| macOS Intel         | `libtv-macos-x64.zip`     |
| Linux x86_64        | `libtv-linux-x64.zip`     |
| Linux arm64         | `libtv-linux-arm64.zip`   |
| Windows x86_64      | `libtv-windows-amd64.zip` |
| Windows arm64       | `libtv-windows-arm64.zip` |

**压缩包内容**：zip 根目录或任一子目录中需包含 **`libtv`** 或 **`libtv.exe`**；脚本解压后在临时目录中查找并复制到安装目录。

走下载需要 **`curl` 或 `wget`**（Windows 上由 PowerShell 的 `Invoke-WebRequest` 负责）；解压需要 **`unzip`**（Windows 上由 `Expand-Archive` 负责）。脚本**不会**用 **`rm`** 清理：解压目录与下载得到的临时 zip 会留在系统临时目录下，可自行删除；安装目标仍由 **`cp -f`（Windows `Copy-Item -Force`）覆盖**以便升级。

---

## macOS / Linux

```bash
chmod +x scripts/install-libtv-cli.sh
./scripts/install-libtv-cli.sh
```

默认安装到 **`~/.libtv/libtv`**。脚本会按 **`$SHELL`** 尝试检测 **`~/.zshrc`**、**`~/.zprofile`**、**`~/.bashrc`** 等（与 [nvm install.sh](https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh) 的 profile 检测类似），若找到且尚未写入过标记行，则**追加**一行 **`export PATH="<安装目录绝对路径>:$PATH"`**；未找到 profile 时只打印需自行追加的两行内容。新开终端或对该文件执行 **`source ~/.zshrc`**（路径以实际为准）后生效。

### 环境变量

| 变量                         | 说明                                                                                                                                                                                                                                                                                                   |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **`LIBTV_CLI_INSTALL_DIR`**  | 安装目录（默认：**`$HOME/.libtv`**；可执行文件为其中的 **`libtv`**）。                                                                                                                                                                                                                                 |
| **`LIBTV_CLI_PROFILE`**      | 指定要追加 PATH 的 **profile 文件绝对路径**；设为 **`/dev/null`** 表示**不写**任何 profile（与 nvm 的 **`PROFILE=/dev/null`** 一致，二者任一即可跳过写入）。                                                                                                                                           |
| **`PROFILE`**                | 若已设为某 profile 路径且文件存在，**优先**于自动检测，用于追加 PATH（与 nvm 行为对齐）。                                                                                                                                                                                                              |
| **`LIBTV_CLI_SKIP_PROFILE`** | 设为 **`1`** 时不修改 profile，仅打印如何把安装目录加入 PATH 的提示。                                                                                                                                                                                                                                  |
| **`LIBTV_CLI_BINARY`**       | 直接指定本地 **`libtv`** 可执行文件的绝对路径（优先级最高，跳过下载与解压）。                                                                                                                                                                                                                          |
| **`LIBTV_CLI_VERSION`**      | 把远端下载 URL 的版本段替换为指定值，即 **`…/cli/<LIBTV_CLI_VERSION>/<zip>`**；未设置则脚本去拉 **`…/cli/latest/manifest.json`** 的 **`.version`** 作为默认版本。仅在临时切换 CLI 版本（不想整体替换 skill）时使用；推荐做法仍是走「安装指定版本」覆盖 skill 包。示例：**`LIBTV_CLI_VERSION=0.0.9`**。 |

---

## Windows

在 **PowerShell** 中进入 skill 根目录后执行：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\install-libtv-cli.ps1
```

或双击 / 在 cmd 中运行 **`scripts\install-libtv-cli.bat`**（内部仍调用 PowerShell）。

也可以不下载 skill 包，直接从官方静态站执行最新安装脚本：

```powershell
Invoke-WebRequest `
  -Uri "https://liblibai-web-static.liblib.cloud/cli/latest/install-libtv-cli.ps1" `
  -UseBasicParsing | Invoke-Expression
```

默认安装到 **`%USERPROFILE%\.libtv\libtv.exe`**。若用户 PATH 中尚未包含 **`%USERPROFILE%\.libtv`**，脚本会**写入当前用户的 Path 环境变量**（需重开终端）；设置 **`LIBTV_CLI_SKIP_PROFILE=1`** 或 **`LIBTV_CLI_PROFILE=/dev/null`** 可跳过写入并仅提示手动添加。

### 环境变量（与 Unix 同名）

| 变量                                                     | 说明                                                                                                            |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `LIBTV_CLI_INSTALL_DIR`                                  | 安装目录。                                                                                                      |
| `LIBTV_CLI_SKIP_PROFILE` / `LIBTV_CLI_PROFILE=/dev/null` | 不写用户 **Path**（见上文）。                                                                                   |
| `LIBTV_CLI_BINARY`                                       | 本地 `libtv.exe` 的绝对路径（优先级最高，跳过下载与解压）。                                                     |
| `LIBTV_CLI_VERSION`                                      | 与 macOS / Linux 一致：覆盖远端下载 URL 的版本段；未设置时脚本去拉 `…/cli/latest/manifest.json` 的 `.version`。 |

---

## 安装指定版本

每个版本的 skill 包（里面就是这套 install 脚本 + `SKILL.md` 等）会按版本号一起发布到：

```
https://liblibai-web-static.liblib.cloud/cli/<version>/libtv-cli-skill.zip
```

**安装步骤**：

1. 下载目标版本的 `libtv-cli-skill.zip`。
2. **整体替换** skill 目录：先**删除**当前 skill 目录，再**新建**同名空目录、把 zip **解压进去**——目的是让 skill 目录与 zip 内容**严格 1:1**，**避免新版本里已删除的旧文件残留**（`unzip -o` / `Expand-Archive -Force` 都**只会覆盖同名文件**，不会清理旧版独有的文件）。
3. **`cd` 切到该 skill 目录**，然后**在该目录下**用 **`LIBTV_CLI_VERSION=<版本号>`** 调起 install 脚本（即 `./scripts/install-libtv-cli.sh` 或 `.\scripts\install-libtv-cli.ps1`），下载到的 `libtv` 才会与该版本严格对应。

> **必须把 `LIBTV_CLI_VERSION` 设成第 1 步的同一个版本号**：未设置 `LIBTV_CLI_VERSION` 时 install 脚本会去拉 `…/cli/latest/manifest.json` 取 `.version` 作为远端默认版本，它**未必**等于你刚下载的 skill 版本（你下载的可能不是 latest）——只有显式传入 `LIBTV_CLI_VERSION`，才能确保 `libtv` 和这套 skill 文档是**同一个版本**。同时**整目录替换** skill、再 `cd` 进去执行脚本：skill 目录里其它文件（`commands/` 等）也需与该版本严格一致。skill 目录不应放任何用户私有文件（`.libtv/` 在 skill 目录的兄弟目录、不会被波及）。

```bash
# macOS / Linux：以安装 0.0.9 为例
VERSION=0.0.9
SKILL_DIR=<你的 skill 目录>            # 即含 SKILL.md / scripts/ 的目录的绝对路径
curl -fL -o /tmp/libtv-cli-skill.zip \
  "https://liblibai-web-static.liblib.cloud/cli/${VERSION}/libtv-cli-skill.zip"
rm -rf "$SKILL_DIR"                    # 删除旧 skill 目录，避免旧文件残留
mkdir -p "$SKILL_DIR"
unzip -q /tmp/libtv-cli-skill.zip -d "$SKILL_DIR"
cd "$SKILL_DIR"                        # 必须在该目录下执行 install 脚本
chmod +x scripts/install-libtv-cli.sh
LIBTV_CLI_VERSION="$VERSION" ./scripts/install-libtv-cli.sh   # 必须传入 LIBTV_CLI_VERSION，确保下载到对应版本的 libtv
```

```powershell
# Windows：以安装 0.0.9 为例
$Version = '0.0.9'
$SkillDir = '<你的 skill 目录>'        # 即含 SKILL.md / scripts\ 的目录的绝对路径
Invoke-WebRequest `
  -Uri "https://liblibai-web-static.liblib.cloud/cli/$Version/libtv-cli-skill.zip" `
  -OutFile $env:TEMP\libtv-cli-skill.zip
Remove-Item -Recurse -Force $SkillDir -ErrorAction SilentlyContinue  # 删除旧 skill 目录
New-Item -ItemType Directory -Path $SkillDir -Force | Out-Null
Expand-Archive -Path $env:TEMP\libtv-cli-skill.zip -DestinationPath $SkillDir -Force
cd $SkillDir                           # 必须在该目录下执行 install 脚本
$env:LIBTV_CLI_VERSION = $Version      # 必须设置，确保下载到对应版本的 libtv
.\scripts\install-libtv-cli.ps1
```

---

## 一键安装完成后

执行 **`libtv --help`**，并按 [SKILL.md](../SKILL.md) 中的 **`libtv login`** 完成登录。
