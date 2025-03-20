# pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple/ openai

import os
import json
import asyncio
from contextlib import AsyncExitStack
from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    
    def __init__(self):
        self.session: ClientSession = None
        self.exit_stack = AsyncExitStack()
        self.openai = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("OPENAI_API_BASE"),
        )
        
    async def connect_to_server(self):

        # 通过 stdio 连接 MCP Server
        server_params = StdioServerParameters(
            command = "python",
            args = ["mcp-server-weather.py"],
            env = None
        )
        self.stdio, self.write = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        await self.session.initialize()

        # 列出所有工具
        response = await self.session.list_tools()
        print("\nConnected to server with tools:", [tool.name for tool in response.tools])
                
    async def chat(self, query: str) -> str:
        
        # 组装 function call 参数
        response = await self.session.list_tools()
        available_tools = [{
            "type": "function",
            "function": {    
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        } for tool in response.tools]

        messages = [{
            "role": "user",
            "content": query,
        }]
        while True:
            print(f"Sending messages {messages}")
            completion = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=available_tools
            )
            tool_calls = completion.choices[0].message.tool_calls
            if tool_calls == None:
                print(completion.choices[0].message.content)
                break
            
            messages.append({
                "role": "assistant",
                "content": "",
                "tool_calls": tool_calls
            })
            
            # 调用工具
            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                tool_args = tool_call.function.arguments
                result = await self.session.call_tool(tool_name, json.loads(tool_args))
                print(f"[Calling tool {tool_name} with args {tool_args}]")
                print(f"[Calling tool result {result.content}]")
            
                messages.append({
                    "role": "tool",
                    "content": result.content,
                    "tool_call_id": tool_call.id
                })

    async def cleanup(self):
        await self.exit_stack.aclose()

async def main():
    client = MCPClient()
    try:
        await client.connect_to_server()
        await client.chat("查下合肥和杭州明天的天气")
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())