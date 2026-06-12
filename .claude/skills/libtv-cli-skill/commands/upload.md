# `libtv upload` — 本地上传为资源节点

把本地文件上传到当前画布项目，并生成 **`image` / `video` / `audio`** 资源节点；之后可用 [`libtv node`](./node.md) 的 `--left/--right` 或管道把该资源节点连到下游。需已登录，见 [`libtv login`](./login.md)；项目范围与 [`libtv project use`](./project.md) 一致。

## 子命令

无子命令，仅 flags。

用法骨架：`libtv upload <节点显示名> [flags]`

### 位置参数

- **`<节点显示名>`**（必填）：上传后生成的**资源节点**在画布上的展示名；应与该画布已有节点不重名，重名时由画布按新建去重。

### 选项

| 选项                                      | 必填       | 说明                                                                                                                                                                                       |
| ----------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `-f, --file <path>` / `--resource <path>` | 二选一必填 | 本地文件绝对 / 相对路径；两 flag 含义相同。                                                                                                                                                |
| `-p, --project <project>`                 | 否         | 目标项目 **UUID**；省略时读当前目录 `.libtv/project.json` 的 `projectUuid`（需已 [`libtv project use`](./project.md)）。**勿与** [`libtv project list -p`](./project.md)（**页码**）混淆。 |
| `-g, --group <group>`                     | 否         | 父级**普通分组**的节点 id 或展示名。新资源节点创建在该组内并写入其 `childNodeIds`。未传时若已 [`libtv group use`](./group.md) 绑定默认分组则自动套用。                                     |
| `-t, --type <type>`                       | 否         | 枚举 `image` / `video` / `audio`；不写则按文件后缀猜测。                                                                                                                                   |
| `--x <n>` / `--y <n>`                     | 否         | 节点坐标（像素）。无 `-g` / 默认分组时为画布绝对坐标；有分组时为**组内相对坐标**。                                                                                                         |
| `--help`                                  | 否         | 打印帮助。                                                                                                                                                                                 |

### 输出

| 流     | 内容                                                                                                                                            |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| stdout | 成功时为 JSON；接到管道时为**一行** NDJSON，含 `nodeKey` 等，便于后续 [`libtv node`](./node.md) / [`libtv group`](./group.md) 通过 stdin 读取。 |
| stderr | 上传过程可能打印进度，前缀 `[upload]` 与百分比。管道与 stdout/stderr 约定见 [../examples/pipes/README.md](../examples/pipes/README.md)。        |

## 示例

```bash
# case 1: 上传图片到当前目录绑定的画布（-p 省略）
libtv upload "参考图" -f ./refs/scene.png

# case 2: 显式指定项目
libtv upload "参考图" -p 11111111-2222-3333-4444-555555555555 --resource ./refs/scene.png

# case 3: 挂到指定普通分组；--x/--y 自动按组内相对坐标
libtv upload "图A" -f ./a.png -g "本镜资源组" --x 80 --y 40

# case 4: 通过 -t 明确文件类型，覆盖后缀推断
libtv upload "旁白音频" -t audio -f ./voice.m4a

# case 5: 上传后把新节点连到下游文本节点（NDJSON 串联）
libtv upload "参考图" -f ./refs/a.png | libtv node "剧情"
```
