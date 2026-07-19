"""Headroom compress() 最小可运行示例。

运行前先安装：
    pip install "headroom-ai[all]"

直接运行：
    python headroom_test.py

这个例子不需要任何 API Key——它只演示压缩本身，不真正调用大模型。
"""

import json

from headroom import compress


def build_messages():
    """构造一段又长又重复的工具输出，模拟 agent 调用工具拿回的结果。

    这里假设 agent 调了一个 list_users 接口，一次返回 200 条结构完全一样的
    用户记录。这种高度同构的 JSON 数组正是 Headroom 最擅长压缩的场景。
    """
    users = [
        {
            "id": i,
            "name": f"user_{i}",
            "email": f"user_{i}@example.com",
            "role": "member",
            "status": "active",
            "created_at": "2026-01-01T00:00:00Z",
        }
        for i in range(200)
    ]
    tool_output = json.dumps({"users": users}, ensure_ascii=False, indent=2)

    # messages 是标准的 Anthropic / OpenAI 消息格式
    return [
        {"role": "user", "content": "帮我看看这批用户里有没有异常状态的。"},
        {"role": "tool", "content": tool_output},
    ]


def main():
    messages = build_messages()

    result = compress(messages, model="claude-sonnet-4-5-20250929")

    print(f"压缩前 token：{result.tokens_before}")
    print(f"压缩后 token：{result.tokens_after}")
    print(f"省下 token：  {result.tokens_saved}")
    print(f"压缩比：      {result.compression_ratio:.2%}")  # 0.65 表示省了 65%
    print(f"用到的压缩器：{result.transforms_applied}")

    # result.messages 是压缩后的消息，格式和输入完全一致，可以直接发给模型：
    #     from anthropic import Anthropic
    #     Anthropic().messages.create(
    #         model="claude-sonnet-4-5-20250929",
    #         messages=result.messages,
    #     )


if __name__ == "__main__":
    main()
