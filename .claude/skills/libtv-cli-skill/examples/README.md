# 常见案例（索引）

本目录下每个 `.md` 是**一个独立 case**，按**场景域**分三组子目录。每个 case 自带**前置条件说明 + 可直接执行的 fenced 代码块**。

## 通用前置条件

以下三条所有 case 默认满足，不在每个文件里重复：

1. 已完成登录（[`libtv login web` / `login phone`](../commands/login.md)）；若用独立凭据目录见 [auth/config-dir.md](./auth/config-dir.md)。
2. 在**画布所在工作目录**执行过 [`libtv project use <项目UUID>`](../commands/project.md)；`libtv project list` 可查 UUID。未绑定时每条命令可显式加 `-p <UUID>`。
3. 需要限定普通分组时执行 [`libtv group use <分组>`](../commands/group.md)；临时覆盖用 `-g/--group`。

语法速查：`-s`（`data.params`）vs `-u`（`data` 顶层）见 [../node-types/README.md](../node-types/README.md)；管道（NDJSON）与 stdout/stderr 规则见 [pipes/README.md](./pipes/README.md)。

## workflow/ — 工作流串联

| 场景                                    | 文件                                                         |
| --------------------------------------- | ------------------------------------------------------------ |
| 上传资源 → 建文本节点 → 连边 → 触发生成 | [workflow/create-and-run.md](./workflow/create-and-run.md)   |
| 一条命令建节点 + 连上游 + 触发生成      | [workflow/all-in-one.md](./workflow/all-in-one.md)           |
| 修改已有节点的生成参数                  | [workflow/update-params.md](./workflow/update-params.md)     |
| 建分组 → 绑定若干子节点 → 整组执行      | [workflow/group-batch-run.md](./workflow/group-batch-run.md) |
| 只连线不改参（确保 / 增量 add / rm）    | [workflow/connect-only.md](./workflow/connect-only.md)       |
| 常见错误对照                            | [workflow/common-errors.md](./workflow/common-errors.md)     |

## node-types/ — 按节点类型

| 类型         | 文件                                                   |
| ------------ | ------------------------------------------------------ |
| `text`       | [node-types/text.md](./node-types/text.md)             |
| `image`      | [node-types/image.md](./node-types/image.md)           |
| `video`      | [node-types/video.md](./node-types/video.md)           |
| `audio`      | [node-types/audio.md](./node-types/audio.md)           |
| `script`     | [node-types/script.md](./node-types/script.md)         |
| `storyboard` | [node-types/storyboard.md](./node-types/storyboard.md) |
| `video-clip` | [node-types/video-clip.md](./node-types/video-clip.md) |

## auth/ — 账号 / 登录

| 场景                           | 文件                                         |
| ------------------------------ | -------------------------------------------- |
| 浏览器登录（可自动打开登录页） | [auth/login-web.md](./auth/login-web.md)     |
| 手机号两步登录                 | [auth/login-phone.md](./auth/login-phone.md) |
| 切换到独立凭据目录再登录       | [auth/config-dir.md](./auth/config-dir.md)   |
| 退出登录                       | [auth/logout.md](./auth/logout.md)           |

## pipes/ — 管道与嵌套用法

| 场景                                                           | 文件                                                 |
| -------------------------------------------------------------- | ---------------------------------------------------- |
| NDJSON / stdout-stderr 概念 + 三 case 索引                     | [pipes/README.md](./pipes/README.md)                 |
| 普通嵌套 → 复杂 DAG（含旁路、`>/dev/null` 抑制、已有节点回放） | [pipes/nested-dag.md](./pipes/nested-dag.md)         |
| 中途报错的退出策略（`&&` / `pipefail` / 并行 `&` 反例 / 清理） | [pipes/error-handling.md](./pipes/error-handling.md) |
| `group` 与 `node` 的嵌套（建组绑定、组内串管道、终剪汇入）     | [pipes/group-and-node.md](./pipes/group-and-node.md) |
