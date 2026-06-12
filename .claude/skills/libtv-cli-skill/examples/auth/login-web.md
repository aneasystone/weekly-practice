# 登录：浏览器方式（`libtv login web`）

**覆盖**：本机起临时 HTTP 服务、打印带 `callback_url` 的登录链接；浏览器完成登录后 CLI 写入 `credentials.json`。详细语义见 [`../../commands/login.md`](../../commands/login.md)。

**前置条件**：本机可开浏览器，或远端 SSH 可把 stderr 打出的登录链接粘到能开浏览器的设备上打开。

```bash
# case A: 自动打开默认浏览器
libtv login web --open

# case B: 自行复制 stderr 里的登录链接（适合远端 / 无桌面环境）
libtv login web
```

关键点：

- 登录成功后 stdout 打印凭据文件路径；失败（超时 / 被关）stderr 报错。
- 如需覆盖登录前缀：`LIBTV_LOGIN_WEB_URL='https://…/zh' libtv login web`，仅改路径用 `LIBTV_LOGIN_WEB_PATH`。
