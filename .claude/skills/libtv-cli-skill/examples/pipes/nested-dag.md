# 管道：嵌套 DAG（从简单到复杂）

**覆盖**：把多个上游 `nodeKey` 经 NDJSON 汇到一个下游节点的左侧；再把这种 fan-in 层层嵌套成 DAG，完整走通「多张图 → 汇总图 → 视频段 → 完片」这种真实链路。

**前置条件**：同 [examples/README.md 的通用前置条件](../README.md#通用前置条件)。

## 简单嵌套（两三个上游汇到一个下游）

```bash
# case A: 已有上游，把它们的 nodeKey 经管道喂给下游的左侧入边
(libtv node "选题" && libtv node "主KV") | libtv node "下游"

# case B: 新建上游并立刻把 NDJSON 接给下游（create 默认往 stdout 吐一行）
(
  libtv node create "选题" -t text --prompt "一段旁白" --set model=aurora-3-prime &&
  libtv node create "主KV" -t image --prompt "9:16 竖版主 KV" --set model=nebula-ultra --set ratio=9:16
) | libtv node create "拼图" -t image \
    --prompt "拼合选题与主 KV" \
    --set model=nebula-ultra --set ratio=9:16 --set modeType=image2image
```

关键行为：

- **NDJSON 每行一个对象**；下游按行解析，取 `nodeKey` / `newNodeKey` 连到左侧（等价 `--left`）。
- `&&` 让左侧失败时不往管道里写，避免污染下游。
- 下游名字必须**唯一匹配**；同名多条会在接到管道时报错。

## 复杂 DAG（嵌套 + 旁路 + stdout 抑制）

真实链路常见长这样：**多张图汇成 D → 旁路一条 audio → 用已有节点再接一条 video → 全部汇进 F**。

下面的骨架照搬自 [`tests/e2e/pipe-use/case-02-dag-nested-kling-seedance-mureka.sh`](../../../../tests/e2e/pipe-use/case-02-dag-nested-kling-seedance-mureka.sh) 的 26–57 行，去掉了时间戳后缀，保留全部管道结构：

```bash
set -euo pipefail

(
  (
    (
      libtv node create "选题" -t text \
        --prompt "60s 都市情感短视频：口播+回音梗+结尾 CTA。" \
        --set model=aurora-3-prime --set count=1 &&
      libtv node create "辅视" -t image \
        --prompt "窄幅横条抽象色带：霓虹粉过渡到电蓝。" \
        --set model=nebula-ultra --set ratio=16:9 --set quality=1K &&
      libtv node create "主KV" -t image \
        --prompt "9:16 竖版主 KV：逆光发丝+地铁玻璃雾面。" \
        --set model=nebula-ultra --set ratio=9:16 --set quality=2K
    ) | libtv node create "拼图D" -t image \
        --prompt "拼合选题、辅视色带与主 KV。" \
        --set model=nebula-ultra --set ratio=9:16 --set quality=2K --set modeType=image2image
  ) && libtv node create "氛围乐" -t audio \
      --prompt "日系钢琴 Loft 感。" \
      --set model=mureka-8 --set scene=Music --set instrumental=1 &&
  (
    ( libtv node "选题" && libtv node "主KV" ) |
      libtv node create "Kling段" -t video \
        --prompt "0–5s：地铁闸机跟拍+口播气口。" \
        --set model=kling-video-o1 --set modeType=mixed2video \
        --set ratio=9:16 --set duration=5 --set quality=high --set count=1
  ) && (
    libtv node "主KV" |
      libtv node create "Seed段" -t video \
        --prompt "由主 KV 静帧单图起幅，轻推轨进站台。" \
        --set model=doubao-seedance-pro --set modeType=singleImage2video \
        --set ratio=9:16 --set resolution=1080P --set duration=5 --set count=1 \
        >/dev/null
  ) && libtv node "主KV"
) | libtv node create "完片F" -t video \
    --prompt "收束 Kling 段、拼图 D 与主 KV 的光色；10s 一体化落版。" \
    --set model="star-video2" --set modeType=mixed2video \
    --set ratio=9:16 --set duration=10 --set resolution=720p --set count=1 \
    >/dev/null
```

逐层读懂这套嵌套的关键手法：

| 手法                                        | 表现                                                                                                                                                                                                       |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | ------------------------------------------------------------------------------------------ |
| \*\*多上游 `&&` 串联 + 外层 `               | ` 汇入\*\*                                                                                                                                                                                                 | `(a && b && c) | d`—— 三个`create`依次成功后，各自 NDJSON 一并进入下游`d` 的 stdin；`d`把它们都当`--left`。 |
| **旁路节点（不进下游管道）**                | 氛围乐 `audio` 用 `&&` 接在主管道之后、但 **不** 出现在外层 `(` 括号里，所以它的 NDJSON 不会流到 `完片F`。适合"建了要留在画布上、但不挂给此下游"的资源节点。                                               |
| **对已有节点做 `libtv node "<名>"` 回放**   | `libtv node "选题"` / `libtv node "主KV"` 不传写参数时**只查询**并吐一行 NDJSON，等价于"在管道里再次引用该节点的 key"，用来把早先层级的节点接到后续下游。                                                  |
| **stdout 抑制：`>/dev/null`**               | `Seed段` 与 `完片F` 的 `create` 结尾加 `>/dev/null`，把它自己的 NDJSON 丢掉；此处用来**不让 Seed 段混进最外层 `完片F` 的 stdin**（否则 F 会误把 Seed 段也当左侧输入）。`完片F` 本身是终点，stdout 也无用。 |
| **中途 `libtv node "主KV"` 作"收尾的一行"** | 外层最后一段 `&& libtv node "主KV"` 让主 KV 的 NDJSON 作为**最后一行**喂给 `完片F`，这样 F 的左侧就是「拼图D + Kling段 + 主KV」而不是「拼图D + Kling段 + Seed段」。                                        |
| **`set -euo pipefail`**                     | 任一 `create` 失败、或管道任一段退出码非 0，整条链立即结束，不会留下"半成品画布"。见 [error-handling.md](./error-handling.md)。                                                                            |

结果检查（可选）：

```bash
libtv project | jq '.nodes | length'   # 期望至少 8 个节点
```

## 什么时候该嵌套、什么时候应该拆成多行脚本

| 场景                                                        | 建议                                                                                                             |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| 上游输出恰好就是下游 `--left` 的来源，**且只用一次**        | 直接管道嵌套，最紧凑。                                                                                           |
| 某个上游**被多个下游复用**（如上面的「主KV」）              | 先 `create` 好，后面用 `libtv node "主KV" \| …` 反复引用；不要重复建。                                           |
| 链路 **跨越多个 `set -e` 生命周期**（中间要人工检查再继续） | 拆成两条脚本或 `git bisect` 式分段执行；长嵌套里中途失败难排错。                                                 |
| 想要**真正并发**加速                                        | **不要**并行写同一个管道（会撞 NDJSON，见 [error-handling.md](./error-handling.md)）；各自写临时文件再顺序合并。 |
