# `libtv script` — 脚本节点相关命令

面向画布上 **`script`** 节点的**跨行批处理**类操作（目前仅「生成分镜图组」）。项目 / 分组范围与 [`libtv node`](./node.md) 一致：通过 **`-p`** / **`-g`** 或 [`libtv project use`](./project.md) / [`libtv group use`](./group.md) 的目录绑定。脚本节点的生成器参数 / 属性语义见 [../node-types/script.md](../node-types/script.md)；管道（NDJSON）、stdout/stderr 约定见 [../examples/pipes/README.md](../examples/pipes/README.md)。

> 创建 / 修改 / 连线脚本节点本身请用 [`libtv node`](./node.md) 并配合 `-t script`；对单个脚本节点触发文本生成也走 [`libtv node "<脚本>" --run`](./node.md)，**不**经本命令。

## 子命令

| 子命令                               | 作用                                                                                                                        |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| **`libtv script storyboard <node>`** | 对齐画布「生成分镜」：校验目标为脚本节点；读已保存的 `imageGenConfig`（可用 `-s` 覆盖）→ 在右侧创建**分镜图组**并逐张生成。 |

完整子命令与选项以 **`libtv script --help`** / **`libtv script storyboard --help`** 为准。

### `libtv script storyboard <node>`

用法骨架：`libtv script storyboard <node> [flags]`

**位置参数**

- **`<node>`**（必填）：目标**脚本节点**的 id 或展示名（**id 优先**、精确匹配）。该节点需已有**分镜行**（`data.rows`）；无行时报错 `没有可分镜的行`，请先 [`libtv node "<脚本>" --run`](./node.md) 生成。

**选项**

| 选项                      | 可重复 | 说明                                                                                                                                                                                                                                                                     |
| ------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `-p, --project <project>` | 否     | 画布项目 UUID；缺省读当前目录 `.libtv/project.json` 的 `projectUuid`（需已 [`libtv project use`](./project.md)）。                                                                                                                                                       |
| `-g, --group <group>`     | 否     | 父级**普通分组**（id 或展示名）：限定 `<node>` 的解析范围只在该组 `childNodeIds` 内；未传时若已 [`libtv group use`](./group.md) 则自动套用。新建的**分镜图组**与其子节点会按画布规则落在脚本节点**右侧**，与此父组的从属关系由画布决定。                                 |
| `-s, --set <key=value>`   | 是     | **覆盖**本次分镜图用的 `imageGenConfig`（模型与生成参数）。规则与 [`libtv node create --set`](./node.md) 完全一致：首个 `=` 拆键值；值可为 `true` / `false` / 数字 / JSON；`settings` 与节点已有值做**浅合并**。未传 `model` 时按 supportModels `scriptImage` 默认首项。 |

**stdin**：不读取。

**行为摘要**

| 阶段                  | 说明                                                                                                                                                                                  |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 校验                  | 目标必须是 `script` 节点；必须已有分镜行（`scriptRowHiddenUuid`）。                                                                                                                   |
| 建组 + 派生分镜图节点 | 在脚本节点右侧创建 **storyboard image 类型的普通分组**（`data.type=group` / `data.storyboardGroupType=image`），并按 `rows` 行数派生同等数量的 **`image`** 子节点，入边来自脚本节点。 |
| 逐张生成              | 对每个分镜图节点按顺序执行与 [`libtv node --run`](./node.md) 同源的生成与轮询；进度打 stderr（约每 3 分钟一条，前缀 `[storyboard image-run]`）。                                      |
| 结果                  | 成功输出分镜组与子节点摘要；任一子图终态为失败（`status=3`）或 run 失败时退出码非 0。                                                                                                 |

**输出**

| 流     | 内容                                                                                                                                                                                                                                                                                                    |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| stdout | 成功时为 JSON，字段包含 `groupNodeKey` / `scriptNodeKey` / `imageNodeKeys[]` / `group`（分组节点详情，`data.type=group`、`data.storyboardGroupType=image`） / `imageGenerationRan`（布尔）/ `imageRuns[]`（每个分镜图子节点的 `{ nodeKey, ok, taskId?, status? }`；`status=2` 成功、`status=3` 失败）。 |
| stderr | 进度与错误：`[storyboard image-run] node=… task=… status=… progress=…%`。                                                                                                                                                                                                                               |

## 示例

```bash
# case 1: 脚本节点已生成分镜行 → 一步建组并逐张生成分镜图（imageGenConfig 用节点已保存值）
libtv script storyboard "剧本"

# case 2: 先写提示词跑文本生成，再生成分镜图组（典型双步流水线）
libtv node create "剧本" -t script --prompt "三幕结构，主角是一名侦探" --set model=aurora-3-prime
libtv node "剧本" --run
libtv script storyboard "剧本"

# case 3: 覆盖本次分镜图模型与比例（不改脚本节点已有 imageGenConfig 的其它键）
libtv script storyboard "剧本" -s model=seedream-4 -s aspectRatio=16:9

# case 4: 显式项目；同时通过 settings 覆盖部分基础设置（浅合并到已有 settings）
libtv script storyboard "剧本" \
  -p 11111111-2222-3333-4444-555555555555 \
  -s 'settings={"ratio":"16:9"}'

# case 5: 常见错误自检
#   - 目标不是 script：报错「<node> 非脚本节点」。
#   - 脚本未 run、无分镜行：报错「没有可分镜的行」；先 libtv node "<脚本>" --run。
#   - 某张分镜图 run 失败：命令退出码非 0，stderr 打该 nodeKey 的失败原因，stdout 的 imageRuns[*].status 会含 3。
```
