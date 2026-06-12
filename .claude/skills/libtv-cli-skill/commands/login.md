# `libtv login` — 登录

把有效凭据写入本机，后续 `libtv` 子命令（凡调远端接口者）会自动携带。凭据目录由 **`LIBTV_CONFIG_DIR`** 控制，默认为 **`~/.libtv`**，内含 **`credentials.json`**；与浏览器 Cookie **`usertoken`** 同源。切换到独立凭据目录见 [`../examples/auth/config-dir.md`](../examples/auth/config-dir.md)。

## 子命令

### `libtv login web`

用法骨架：`libtv login web [flags]`

本机起一个临时 HTTP 服务，stderr 打印带 **`callback_url`** 的 LibTV 首页链接；在浏览器完成登录后跳回 **`http://127.0.0.1:<端口>/callback?token=…`**，CLI 校验并把凭据写入 **`credentials.json`**。

**位置参数**：无。

**选项**：

| 选项     | 必填 | 说明                                                                                                   |
| -------- | ---- | ------------------------------------------------------------------------------------------------------ |
| `--open` | 否   | 尝试用系统默认浏览器打开登录链接（macOS `open`、Windows `start`、其它 `xdg-open`）。未设时仅打印链接。 |
| `--help` | 否   | 打印该子命令帮助。                                                                                     |

**相关环境变量**（与 `web` 登录页地址拼装相关）：

| 环境变量               | 作用                                                                            |
| ---------------------- | ------------------------------------------------------------------------------- |
| `LIBTV_LOGIN_WEB_URL`  | **整段**覆盖登录前缀（含域名 + 路径）；设此项时 `LIBTV_LOGIN_WEB_PATH` 被忽略。 |
| `LIBTV_LOGIN_WEB_PATH` | 只改路径；拼在默认域名（`config.tv.domain`）后。                                |

> 两者都未设时使用内建的 **`config.tv.domain` + `/zh`**。

**输出**：成功时 stdout 打印凭据文件路径；stderr 会打印待打开的登录链接与等待提示。失败时 stderr 报错，退出码非 0。

### `libtv login phone`

用法骨架：`libtv login phone -p <11位手机号> [-c <6位验证码>] [--platform <x>] [--captcha <json>]`

**两步流程**：

1. **发短信**（不传 `-c`）：`libtv login phone -p <手机号>`；若提示「需要人机验证」，在网页完成验证后把接口要求的参数经 **`--captcha`** 传回并重试第 1 步。
2. **带验证码完成登录**：`libtv login phone -p <手机号> -c <6位验证码>`。

**位置参数**：无。

**选项**：

| 选项                       | 必填            | 说明                                                         |
| -------------------------- | --------------- | ------------------------------------------------------------ |
| `-p, --phone <11位手机号>` | 是              | 登录的手机号。                                               |
| `-c, --code <6位验证码>`   | 第 2 步必填     | 第 1 步（发短信）**不要传**；第 2 步凭短信验证码传入。       |
| `--platform <x>`           | 否              | 平台标识，一般保持默认。                                     |
| `--captcha <json>`         | 仅第 1 步触发时 | 第 1 步提示「需要人机验证」时，把浏览器返回的 payload 传回。 |
| `--help`                   | 否              | 打印该子命令帮助。                                           |

**输出**：同 `login web`；失败（如频控 / 封禁 / 验证码错）会在 stderr 打印原因，退出码非 0。

## 示例

```bash
# case 1: 浏览器方式登录，并尝试自动打开登录页
libtv login web --open

# case 2: 浏览器方式登录，自行复制 stderr 里的链接粘到其它机器
libtv login web

# case 3: 手机号两步登录
libtv login phone -p 13800138000
libtv login phone -p 13800138000 -c 123456

# case 4: 把凭据存到自定义目录（下同一 shell 内所有 libtv 子命令也会读这里）
LIBTV_CONFIG_DIR="$HOME/.libtv-dev" libtv login web

# case 5: 覆盖登录页前缀（仅 web 登录）
LIBTV_LOGIN_WEB_URL='https://www.liblib.art/tv/zh' libtv login web
```
