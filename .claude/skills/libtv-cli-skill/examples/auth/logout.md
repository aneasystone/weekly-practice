# 退出登录（`libtv logout`）

**覆盖**：清掉本机 `credentials.json` 与当前进程内存中的凭据快照。详细语义见 [`../../commands/logout.md`](../../commands/logout.md)。

**前置条件**：已登录过，或不确定是否登录。

```bash
# case A: 退出登录（默认凭据目录 ~/.libtv）
libtv logout

# case B: 针对自定义凭据目录退出登录
LIBTV_CONFIG_DIR="$HOME/.libtv-dev" libtv logout
```

关键点：

- stdout 返回 JSON：`{ credentialsPath, loggedOut: true }`。即使凭据文件不存在也以「已登出」处理、退出码 0。
- 需要切到其它账号时：`libtv logout` → 再 [`libtv login web`](./login-web.md)（或 [`login-phone.md`](./login-phone.md)）。
