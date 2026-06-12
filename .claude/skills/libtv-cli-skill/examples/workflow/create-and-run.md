# 工作流：上传资源 → 建文本节点 → 连边 → 触发生成

**覆盖**：多步组合（分三条命令写清楚每一步）。展示 `libtv upload` / `libtv node` 默认用法的基本组合。

**前置条件**（附加于 [README.md 的通用前置条件](../README.md#通用前置条件) 之上）：

- 本地有一张参考图 `./refs/scene.png`。

```bash
# 1) 上传一张图片为资源节点（挂在画布上）
libtv upload "参考图" -t image --resource ./refs/scene.png

# 2) 新建一个文本节点并写好提示词与模型
libtv node "剧情" -t text --prompt "根据参考图写一段分镜旁白" --set model=aurora-3-prime

# 3) 把「参考图」连到「剧情」左侧——两种等价写法
libtv node "剧情" --left 参考图          # 方法 A：按显示名
libtv node "参考图" | libtv node "剧情"  # 方法 B：stdin 串联上游 nodeKey

# 4) 节点已存在、无改参时，仅触发一次生成
libtv node "剧情" --run
```

把这 4 步压成一条命令的写法见 [all-in-one.md](./all-in-one.md)。
