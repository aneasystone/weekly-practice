# `video` — 视频节点（以 Seedance 2.0 `star-video2` 为例）

**覆盖**：混合模式（图+文 → 视频）建节点、挂两张参考图、触发生成、改封面。字段语义以 [`../../node-types/video.md`](../../node-types/video.md) 为准。

**前置条件**：同 [../README.md 的通用前置条件](../README.md#通用前置条件)；本地有 `./refs/a.png` 和 `./refs/b.png`。

```bash
# 1) 先把参考图作为 image 资源节点挂上来
libtv upload "参考图1" -t image --resource ./refs/a.png
libtv upload "参考图2" -t image --resource ./refs/b.png

# 2) 建一个视频节点（mixed2video 需要至少 1 张参考图）
libtv node "镜头A" -t video --prompt "无人机掠过海面" \
  --set model=star-video2 \
  --set modeType=mixed2video \
  --set count=1 \
  --set ratio=16:9 \
  --set resolution=720p \
  --set duration=5 \
  --set enableSound=on \
  --set search_enabled=1 \
  --left 参考图1 --left 参考图2 \
  --run

# 3) 仅改封面缩略图（不影响生成）
libtv node "镜头A" -u poster='https://.../cover.jpg'
```

关键点：

- `modeType` 决定 **`modeType.items`** 上限（参考图数量）；越界会在 CLI 校验期直接拒绝。
- 生成新结果后会追加到 `data.results`；改封面请走 `-u poster=…`，不要用 `-s`。
