# 管道：`group` 与 `node` 的嵌套

**覆盖**：把 `libtv group create` 的 NDJSON 直接喂给 `libtv group use -r`，一条管道绑好 `groupNodeKey`；然后在组内串 `libtv node create`，用管道把多个上游节点挂进下游，并用 `libtv group … --run` 整组触发。

**前置条件**：同 [examples/README.md 的通用前置条件](../README.md#通用前置条件)；已 `libtv project use <项目UUID>`。

## 建组 + 绑定（管道一条命令搞定）

```bash
set -euo pipefail

# case A: 建组 → 绑定当前目录到该组（省去后续 -g）
libtv group create 首集分镜 | libtv group use -r
```

要点：

- `libtv group create` 的 stdout 接到管道时吐 NDJSON（含 `newNodeKey`）。
- `libtv group use -r` 的 `-r` 语义是**从 stdin 读取 key**（不是 `--run`）；它把该 key 写入当前目录 `.libtv/project.json` 的 `groupNodeKey`。
- 绑定后，后续 `libtv node` 未显式传 `-g` / `-p` 时**默认落在该组内**。
- 解除绑定：`libtv group unuse`。完整 `group` 子命令见 [../../commands/group.md](../../commands/group.md)。

## 组内用管道批量建节点

绑定分组后，直接在组内串管道，一次把「大纲 → 资产板 → 汇总」这种链路建完：

```bash
libtv group create 首集分镜 | libtv group use -r

(
  libtv node create "大纲" -t text \
    --prompt "12 集网剧 bible：双主角、主线副线、视觉关键词。" \
    --set model=aurora-3-prime --set count=1 &&
  libtv node create "角-三视图" -t image \
    --prompt "女主三视图 T-pose：正/侧/背，灰蓝套裙。" \
    --set model=nebula-ultra --set ratio=16:9 --set quality=2K &&
  libtv node create "角-服饰" -t image \
    --prompt "灰蓝风衣+衬衫+直筒西裤+帆布鞋，布料厚度单独标注。" \
    --set model=nebula-ultra --set ratio=16:9 --set quality=2K
) | libtv node create "角-汇总" -t image \
    --prompt "角色资产蒙太奇：拼合三视图/服饰，附比例尺与色条。" \
    --set model=nebula-ultra --set modeType=image2image --set ratio=16:9 --set quality=2K
```

要点：

- 所有 `libtv node create` 都**不写 `-g`**：既然已 `group use`，默认就在 `首集分镜` 组内。
- `(a && b && c) | d` 把三个上游的 NDJSON 一并喂给 `角-汇总`，等价于 `d --left a --left b --left c`。
- 想**临时跳出当前组**（只绑项目、不进组），一次命令加 `-g ""` 或换用 `-p <projectUuid>` 不要 `-g`；也可以 `libtv group unuse` 后再跑。

## 用 `--node` 把已有节点显式挂进组 + 整组触发

如果节点在建的时候没落进当前组（例如是别的脚本先建的），用 `group <组名> --node` 一次性收编；批量建好后再 `--run` 整组触发：

```bash
# case A: 把已有的 3 个镜头节点挂进分组
libtv group 首集分镜 --node 镜头A --node 镜头B --node 镜头C

# case B: 查看组里当前有哪些子节点
libtv group 首集分镜 --list

# case C: 整组触发生成（组内所有子节点各跑一次）
libtv group 首集分镜 --run
```

## 管道里混用 `node` 与 `group`

可以在管道里把「组内某几个节点」与「新建节点」混着喂给下一个下游——常见于剧集终剪：先在组里挨个建好分镜视频，再把它们和一条音频一起汇进 `video-clip` 终剪节点。

```bash
# 前置：画布上已有 "镜-01"/"镜-02"/"镜-03" 三个视频节点、"首集分镜" 是当前组
{
  libtv node "镜-01"
  libtv node "镜-02"
  libtv node "镜-03"
  libtv node create "BGM" -t audio \
    --prompt "轻弦乐+单音钢琴，为终剪铺底，不进副歌。" \
    --set model=mureka-8 --set scene=Music --set instrumental=1
} | libtv node create "终剪" -t video-clip \
    --prompt "硬切对齐镜 01/02/03；BGM duck 在口播位；尾 0.5s 淡出。" \
    >/dev/null
```

要点：

- `{ …; …; } | 下游` 与 `( … && … ) | 下游` 的区别：**`{}` 不要求前面那条成功再执行下一条**——适合"都是已存在节点的查询"（只读场景失败概率低）；涉及 `create` 这种有副作用的写操作时**用 `&&`**。
- `终剪` 的 `>/dev/null` 把它自己的 NDJSON 丢掉，因为没有后续下游再消费它了。
- 上面这段骨架来自真实脚本 [`tests/e2e/pipe-use/case-03-pipeline-outline-assets-storyboard-clip.sh`](../../../../tests/e2e/pipe-use/case-03-pipeline-outline-assets-storyboard-clip.sh) 的 `剧·终剪` 段。
