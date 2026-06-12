# `audio` — 音频 / 语音节点

**覆盖**：语音配音（需 `voice`）和纯乐器 BGM（`instrumental=1`）两种模型的最小生成命令。字段语义以 [`../../node-types/audio.md`](../../node-types/audio.md) 为准。

**前置条件**：同 [../README.md 的通用前置条件](../README.md#通用前置条件)。

```bash
# case A: 语音（TTS 类）—— 需要 voice（音色 ID）
libtv node "配音" -t audio --prompt "沉稳男声，语速偏慢" \
  --set model=vocal-v3 \
  --set voice=某音色ID \
  --set stability=0.5 \
  --run

# case B: 纯乐器（BGM）—— 用 instrumental=1 关掉人声
libtv node "片尾曲" -t audio --prompt "电影片尾，弦乐渐强" \
  --set model=mureka-8 \
  --set instrumental=1 \
  --run
```
