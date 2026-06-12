# `video-clip` — 视频合成节点

**覆盖**：建空合成节点、用 `-u` 维护时间线数据与裁剪范围、最后触发一次合成。字段语义以 [`../../node-types/video-clip.md`](../../node-types/video-clip.md) 为准。

**前置条件**：同 [../README.md 的通用前置条件](../README.md#通用前置条件)。

```bash
# 1) 先建一个空的合成节点（--run 前需要先补齐时间线）
libtv node "视频合成" -t video-clip

# 2) 维护合成参数（都走 -u、写 data 顶层）
libtv node "视频合成" -u cropRange='[0.2,8.5]'
libtv node "视频合成" -u clipTimelineData='{"videoSourceNodeIds":["..."],"audioSourceNodeIds":[],"clips":[],"totalDuration":10,"currentTime":0,"scale":1,"scrollX":0}'

# 3) 触发一次合成
libtv node "视频合成" --run
```

关键点：

- `video-clip` **没有 `data.params`**，`-s/--set` 在此节点上会被拒绝（只允许 `-u`）。
- `clipTimelineData` 为单字段 JSON；深层结构如 `clips` 需整块替换。
- `cropRange` 是两元素数组 `[起, 止]`，单位为秒，需满足 `起 < 止 ≤ totalDuration`。
