# 管道：中途报错的退出策略

**覆盖**：管道里任一段 `create` 失败时，如何让整条链**立即停住、且不被静默吞掉**，避免画布上留下一堆"一半成功"的节点。

**前置条件**：同 [examples/README.md 的通用前置条件](../README.md#通用前置条件)。

## 推荐默认：`set -euo pipefail` + `&&`

脚本放最前面这行（[案例](../../../../tests/e2e/pipe-use/case-02-dag-nested-kling-seedance-mureka.sh) 里就是这么开场的）：

```bash
set -euo pipefail
```

| 开关          | 作用                                                                                                             |
| ------------- | ---------------------------------------------------------------------------------------------------------------- |
| `-e`          | 任一命令退出码非 0，脚本**立即**终止（不再执行后续行）。                                                         |
| `-u`          | 引用未定义变量直接报错（避免把 `${UUID}` 打错成 `${UID}` 跑出奇怪结果）。                                        |
| `-o pipefail` | **管道**的退出码取**最早失败的那一段**，而不是只看最右端；没它的话 `a \| b` 里 `a` 失败但 `b` 成功，整条仍为 0。 |

然后所有层级的"依次执行"一律用 `&&`，不要用 `;`：

```bash
# ✅ 左侧失败则立刻停，不会把错误 stdout 喂给下游
(
  libtv node create "选题" -t text --prompt "…" --set model=aurora-3-prime &&
  libtv node create "主KV" -t image --prompt "…" --set model=nebula-ultra --set ratio=9:16
) | libtv node create "拼图" -t image --prompt "…" --set model=nebula-ultra --set modeType=image2image

# ❌ 用 ;：前者失败后者照跑，管道里塞进半残的 NDJSON，下游报解析错误
(
  libtv node create "选题" -t text --prompt "…" --set model=aurora-3-prime ;
  libtv node create "主KV" -t image --prompt "…" --set model=nebula-ultra --set ratio=9:16
) | libtv node create "拼图" -t image --prompt "…" --set model=nebula-ultra --set modeType=image2image
```

## 并行 `&` 和管道互斥——别用

多个进程同时往**同一条管道**写 NDJSON 时，一行 JSON 的字节会被**另一行穿插进来**，下游按行 `JSON.parse` 直接炸：

```bash
# ❌ 反例：两个 create 并行写同一管道，下游解析 50% 失败
(libtv node "上游甲" & libtv node "上游乙" &) | libtv node "下游"

# ✅ 修法 1：顺序执行
(libtv node "上游甲" && libtv node "上游乙") | libtv node "下游"

# ✅ 修法 2：需要并发就各写各的文件，最后顺序合并
tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT
libtv node "上游甲" >> "$tmp" &
libtv node "上游乙" >> "$tmp" &
wait
cat "$tmp" | libtv node "下游"
```

> `&` 和管道能不混用就不混用；真要并发，让每个上游各写独立文件，再在串行步骤里合并喂下游。

## 保留 stderr，否则失败看不到原因

`libtv` 把业务结果 JSON / NDJSON 吐到 **stdout**，把进度、鉴权失败、轮询提示等吐到 **stderr**。写脚本时：

```bash
# ✅ stderr 单独落日志，stdout 正常接管道
( (libtv node "上游甲" && libtv node "上游乙") | libtv node "下游" --run ) 2>> pipeline.log

# ❌ 一刀 2>/dev/null：失败时拿不到任何线索
libtv node "上游甲" 2>/dev/null | libtv node "下游"
```

## 失败后的现场清理

启用 `-e` 时脚本在失败那行就停了，画布上可能已经有"成功了一半"的节点。两种常见处理：

```bash
# 方式 1：trap EXIT 打印现场，方便复盘（不改行为）
trap 'echo "[pipeline] exit=$? 最新节点见 libtv node list" >&2' EXIT

# 方式 2：脚本失败后重跑前清场——删除这次生成的节点
#   前提：给节点加统一前缀/时间戳，便于 jq 过滤后批删
libtv node list | jq -r '.nodes[] | select(.name | startswith("剧·")) | .nodeKey' \
  | while read -r k; do libtv node delete "$k"; done
```

| 现象                                              | 原因 / 修复                                                                                                             |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| 管道下游报 `invalid json on line N`               | 上游里混了并行 `&`，或上游把非 JSON 文本误打到 stdout。改串行；并检查上游是否被 `;` 串错。                              |
| `set -e` 下整条脚本静默跑完，但画布只有前几个节点 | 少写了 `-o pipefail`；管道某段失败被右端成功掩盖。补 `set -o pipefail`。                                                |
| 偶发"成功但下游说找不到上游"                      | 上游用 `>/dev/null` 把 NDJSON 丢了，下游自然读不到 key。去掉那处 `>/dev/null`。                                         |
| 401 / AUTH\_\* / PROJECT_NOT_BOUND                | 凭据或项目绑定问题，见 [auth/config-dir.md](../auth/config-dir.md) / [commands/project.md](../../commands/project.md)。 |
