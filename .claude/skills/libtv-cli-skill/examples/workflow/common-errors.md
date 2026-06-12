# 工作流：常见错误对照

**覆盖**：几个最容易踩的失败形态，**左错右对**。错误在 stderr 输出，退出码非 0；成功写法在 stdout 返回 NDJSON。

**前置条件**：同 [README.md 的通用前置条件](../README.md#通用前置条件)。

```bash
# case 1: 试图用 -u 写 data.params —— 被拒绝
libtv node "剧情" -u params.prompt="走起"                # ❌ 非法：params 属于生成参数
libtv node "剧情" --set prompt="走起"                    # ✅ 用 --set

# case 2: 试图用 -u 改 key —— 被拒绝
libtv node "剧情" -u key=new-key                         # ❌ key 禁止改
# 如需替换主键，删除重建：libtv node "剧情" --delete && libtv node create …

# case 3: 同一命令同时写 --left 与 --left-add —— 被拒绝
libtv node "剧情" --left A --left-add B                  # ❌ 模式冲突
libtv node "剧情" --left A --left B                      # ✅ 整体对齐
libtv node "剧情" --left-add B                           # ✅ 仅追加

# case 4: --set 写到不属于当前节点类型 schema 的键 —— 被拒绝（校验期）
libtv node "剧情" --set ratio=16:9                       # ❌ text 没有 ratio
# 查该类型接受哪些键：libtv model search --type text

# case 5: 未登录或凭据过期
libtv node list                                          # ❌ 401 / AUTH_*
libtv login web --open                                   # ✅ 重新登录

# case 6: 未绑定项目又没给 -p
libtv node list                                          # ❌ PROJECT_NOT_BOUND
libtv project use <项目UUID>                             # ✅ 绑定后再跑
libtv -p <项目UUID> node list                           # ✅ 或临时覆盖
```
