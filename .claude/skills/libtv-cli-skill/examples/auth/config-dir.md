# 登录：切换到独立凭据目录（`LIBTV_CONFIG_DIR`）

**覆盖**：通过 `LIBTV_CONFIG_DIR` 把凭据（`credentials.json`）与本地项目 / 分组绑定（`.libtv/project.json`）指向自定义目录，适合多账号 / 测试环境隔离。`LIBTV_CONFIG_DIR` 语义见 [`../../commands/login.md`](../../commands/login.md)。

**前置条件**：有想要隔离的新账号或测试环境账号。

```bash
# 1) 只为一次命令切换凭据目录
LIBTV_CONFIG_DIR="$HOME/.libtv-dev" libtv login web

# 2) 整个 shell 都切换（写到 ~/.zshrc / ~/.bashrc 可常驻）
export LIBTV_CONFIG_DIR="$HOME/.libtv-dev"
libtv login web
libtv project list
libtv logout         # 仅清 $HOME/.libtv-dev 下的 credentials.json

# 3) 还原到默认目录（~/.libtv）
unset LIBTV_CONFIG_DIR
```

关键点：

- `LIBTV_CONFIG_DIR` 不影响网络请求，只影响**本机状态写入位置**（凭据 + 项目 / 分组绑定）。
- 和浏览器 Cookie 同源——默认目录的身份与你在 `https://www.liblib.art` 登录的身份一致。
