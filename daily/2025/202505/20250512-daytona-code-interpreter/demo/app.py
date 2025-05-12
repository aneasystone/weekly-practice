from dotenv import load_dotenv
load_dotenv()

import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
DAYTONA_API_KEY = os.getenv("DAYTONA_API_KEY")

import json
import requests
from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

from daytona_sdk import Daytona, DaytonaConfig, CreateSandboxParams
daytona = Daytona(DaytonaConfig(api_key=DAYTONA_API_KEY))

tools = [
    {
        "type": "function",
        "function": {
            "name": "code_interpreter",
            "description": "生成 Pytohn 代码并执行，用于解决用户提出的数学或代码类问题",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "用户问题",
                    }
                },
                "required": ["query"],
            }
        }
    }
]

def execute_code(code):
    params = CreateSandboxParams(
        language="python"
    )
    sandbox = daytona.create(params)
    response = sandbox.process.code_run(code)
    if response.exit_code != 0:
        return f"Error running code: {response.exit_code} {response.result}"
    else:
        return response.result

def generate_code(query):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": "你是一个 Python 编码助手，请生成一段 Python 代码解决用户的问题，直接输出代码，不用解释。"
            },
            {
                "role": "user",
                "content": query,
            },
        ],
    )
    return completion.choices[0].message.content

def code_interpreter(args):
    result = generate_code(args['query'])
    print("生成代码：", result)
    
    import re
    code_match = re.search(r"```python\n(.*?)```", result, re.DOTALL)
    code = code_match.group(1) if code_match else result
    code = code.replace('\\', '\\\\')
    
    result = execute_code(code)
    print("代码执行结果：", result)
    return result

def chat_completion_with_function_calling(query):
    messages=[
        {'role': 'user', 'content': query},
    ]
    while True:
        # print(messages)
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
        )
        # print(completion)
        message = completion.choices[0].message
        if not message.tool_calls:
            break

        # append messages
        tool_calls = message.tool_calls
        messages.append(
            {'role': 'assistant', 'tool_calls': tool_calls, 'content': ''},
        )
        
        # do function calling
        for tool_call in tool_calls:
            function = globals().get(tool_call.function.name)
            args = json.loads(tool_call.function.arguments)
            result = function(args)
            # print(result)
            messages.append(
                {'role': 'tool', 'content': result, 'tool_call_id': tool_call.id},
            )
    return completion

# completion = chat_completion_with_function_calling('你好')
# print(completion.choices[0].message.content)

completion = chat_completion_with_function_calling('斐波拉契数列的第20项是多少？')
print(completion.choices[0].message.content)