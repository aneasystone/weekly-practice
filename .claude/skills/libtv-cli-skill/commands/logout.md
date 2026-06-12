# `libtv logout` — 退出登录

清除本机上由 `[libtv login](./login.md)` 写入的凭据：删除 `**LIBTV_CONFIG_DIR**`（默认 `**~/.libtv**`）下的 `**credentials.json**`，并清除当前进程中的内存凭据快照。

## 子命令

无子命令，仅 flags。

用法骨架：`libtv logout [flags]`

**位置参数**：无。

**选项**：

- `**--help`\*\* — 打印帮助。

**输出**：stdout 为 JSON，含 `**credentialsPath`**、`**loggedOut: true\*\*`。若凭据文件本不存在，仍会按「已登出」处理，返回同结构 JSON，退出码为 0。

## 示例

```bash
# case 1: 退出登录（默认凭据目录 ~/.libtv）
libtv logout

# case 2: 针对自定义凭据目录退出登录
LIBTV_CONFIG_DIR="$HOME/.libtv-dev" libtv logout
```
