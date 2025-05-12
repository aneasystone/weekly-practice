from dotenv import load_dotenv
load_dotenv()

import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")

import json
from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_date",
            "description": "获取今天的日期信息，包括几月几号和星期几",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather_info",
            "description": "获取某个城市某一天的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名",
                    },
                    "date": {
                        "type": "string",
                        "description": "日期，格式为 yyyy-MM-dd",
                    },
                },
                "required": ["city", "date"],
            }
        }
    }
]

def get_current_date(args):
    import datetime
    today = datetime.date.today()
    weekday = today.weekday()
    weeekdays = ['一','二','三','四','五','六','日']
    return '今天是' + str(today) + ', ' + '星期' + weeekdays[weekday]

def get_weather_info(args):
    import requests
    import json
    day = args['date'].split('-')[2]
    url = 'https://query.asilu.com/weather/baidu/?city=' + args['city']
    content = requests.get(url).content
    response = json.loads(content.decode())
    for weather in response['weather']:
        if day == weather['date'].split('日')[0]:
            return weather['weather'] + "，" + weather['temp'] + "，" + weather['wind']
    return '未查询到天气'

def chat_completion_with_function_calling(query):
    messages=[
        {'role': 'user', 'content': query},
    ]
    while True:
        print(messages)
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
        )
        print(completion.to_json())
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

# completion = chat_completion_with_function_calling('今天是几号？')
# print(completion.choices[0].message.content)

# completion = chat_completion_with_function_calling('昨天是星期几？')
# print(completion.choices[0].message.content)

completion = chat_completion_with_function_calling('明天合肥的天气怎么样？')
print(completion.choices[0].message.content)

# completion = chat_completion_with_function_calling('昨天合肥的天气怎么样？')
# print(completion.choices[0].message.content)
