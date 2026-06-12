# `image` — 图片节点

**覆盖**：上传参考图作为资源节点、建图片生成节点、连参考图、改节点属性。字段语义以 [`../../node-types/image.md`](../../node-types/image.md) 为准。

**前置条件**：同 [../README.md 的通用前置条件](../README.md#通用前置条件)；本地有 `./refs/ref.png`。

```bash
# 1) 上传本地图作为资源节点（画布上一个 image 节点）
libtv upload "参考图" -t image --resource ./refs/ref.png

# 2) 建一个图片生成节点，并连参考图
libtv node "概念图" -t image --prompt "赛博朋克街景" \
  --set model=nebula-ultra \
  --set ratio=16:9 \
  --set quality=2K \
  --set searchable=1 \
  --left 参考图

# 3) 只改节点自身属性，不影响生成参数（走 -u，写 data 顶层）
libtv node "概念图" -u rotateAngle=90 -u alt="封面示意"
```
