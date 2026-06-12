# 登录：手机号两步（`libtv login phone`）

**覆盖**：发短信（无 `-c`）→ 带验证码完成登录（有 `-c`）两步；若提示人机验证则通过 `--captcha` 传回所需参数。详细语义见 [`../../commands/login.md`](../../commands/login.md)。

**前置条件**：能收到该手机号的短信验证码。

```bash
# 1) 发短信（不传 -c）
libtv login phone -p 13800138000

# 2) 带 6 位验证码完成登录
libtv login phone -p 13800138000 -c 123456

# 额外：需要人机验证时，第 1 步重试时带 --captcha <json>
# libtv login phone -p 13800138000 --captcha '{"…":"…"}'
```

关键点：

- 第 1 步的「需要人机验证」由 stderr 明确提示；拿到浏览器返回的验证 payload 再重跑第 1 步。
- 第 2 步成功后同 `login web`：stdout 打印凭据路径，`credentials.json` 落地。
