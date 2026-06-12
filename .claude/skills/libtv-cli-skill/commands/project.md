# `libtv project` — 画布项目

创建、查询远程画布项目，以及**把当前工作目录绑定到某个项目**（写入 `.libtv/project.json`）。多数子命令（[`libtv node`](./node.md)、[`libtv upload`](./upload.md)、[`libtv group`](./group.md)）在未传 `-p/--project` 时会读取该文件里的 **`projectUuid`**；未绑定且未传 `-p` 时会报错并提示执行 `libtv project use`。

`.libtv/project.json` 写在当前工作目录；stdout/stderr 与管道嵌套 case 见 [../examples/pipes/README.md](../examples/pipes/README.md)。

## 子命令

| 子命令                                    | 作用                                                          |
| ----------------------------------------- | ------------------------------------------------------------- |
| **`libtv project create <project>`**      | 新建空白画布项目                                              |
| **`libtv project list`**（别名 **`ls`**） | 分页列出当前账号下的画布项目                                  |
| **`libtv project use <projectUuid>`**     | 把当前目录绑定到指定项目                                      |
| **`libtv project unuse`**                 | 解除当前目录与项目的绑定                                      |
| **（默认）`libtv project [projectUuid]`** | 拉取画布详情并输出**精简 JSON**（节点、边、id、展示名、位置） |

### `libtv project create <project>`

用法骨架：`libtv project create <project> [flags]`

**位置参数**

- **`<project>`**（必填）：项目名称（展示用）；含空格时用引号。

**选项**

| 选项                       | 必填 | 说明                          |
| -------------------------- | ---- | ----------------------------- |
| `-d, --description <text>` | 否   | 项目简介。                    |
| `--cover-url <url>`        | 否   | 封面图 URL。                  |
| `-t, --team-id <n>`        | 否   | 团队场景下的团队 ID（整数）。 |
| `--help`                   | 否   | 打印该子命令帮助。            |

**输出**：stdout 为 JSON，含新项目信息（可从中取 `uuid` 供后续 `libtv project use` 或其它子命令的 `-p` 使用）。

### `libtv project list`（别名 `ls`）

用法骨架：`libtv project list [flags]`

**位置参数**：无。

**选项**

| 选项                     | 默认              | 说明                                                                                |
| ------------------------ | ----------------- | ----------------------------------------------------------------------------------- |
| `-p, --page <n>`         | `1`               | **页码**（从 1 起）。⚠️ **不是项目 UUID**，勿与 [`libtv node -p`](./node.md) 混淆。 |
| `-s, --page-size <n>`    | `20`              | 每页条数。                                                                          |
| `-o, --order-by <field>` | `updated_at_desc` | 排序，须为接口约定值之一：`updated_at_desc` / `edit_time_desc` / `edit_time_asc`。  |
| `--name <text>`          | —                 | 仅保留名称**包含**该关键字的项（子串匹配）。                                        |
| `--help`                 | —                 | 打印帮助。                                                                          |

**输出**：stdout 为 JSON。

### `libtv project use <projectUuid>`

用法骨架：`libtv project use <projectUuid> [flags]`

**位置参数**

- **`<projectUuid>`**（必填）：**仅支持项目 UUID**（不支持按名称模糊匹配）。会先调接口校验可访问，再写入本地 `.libtv/project.json`。

**选项**

- **`--help`** — 打印帮助。

**副作用**：**会清除**该文件中原有的 **`groupNodeKey`**（默认分组绑定）；仍需组内限定请重新执行 [`libtv group use`](./group.md)。

**输出**：stdout 为 JSON，含 `cwd`、`projectUuid`；校验成功时可能含 `name`。

### `libtv project unuse`

用法骨架：`libtv project unuse`

**位置参数**：无。**选项**：仅 `--help`。

**副作用**：**删除** `.libtv/project.json`（含其中的 `groupNodeKey` 一并移除）。

**输出**：stdout 为 JSON，如 `{ "unbound": true }`。

### `libtv project` / `libtv project <projectUuid>`（默认子命令）

用法骨架：`libtv project [projectUuid]`

**位置参数**

- **`[projectUuid]`**（可选）：项目 UUID；省略时使用当前目录 `.libtv/project.json` 的 `projectUuid`；未绑定且未传参则报错。

**输出**：stdout 为 JSON——节点 id / 展示名 / 类型 / 位置；边的 id / source / target。便于快速查看项目画布结构，**不等价**于完整的项目元数据接口。

## 示例

```bash
# case 1: 新建项目，然后立刻绑定到当前目录
NEW=$(libtv project create "测试画布" -d "demo" | jq -r '.uuid')
libtv project use "$NEW"

# case 2: 翻页列出我的项目（页码走 -p/--page，不是 UUID）
libtv project list -p 1 -s 20

# case 3: 按名称子串过滤
libtv project list --name "分镜"

# case 4: 仅需画布结构（节点 + 边）时的快速摘要
libtv project                # 省略 UUID：使用目录绑定
libtv project 11111111-2222-3333-4444-555555555555

# case 5: 解除当前目录的项目绑定（同时清除 groupNodeKey）
libtv project unuse
```
