import os
import openai
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

functions = [
    {
        "name": "get_current_date",
        "description": "获取今天的日期信息，包括几月几号和星期几",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
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
]

completion = openai.ChatCompletion.create(
    temperature=0.7,
    model="gpt-3.5-turbo",
    messages=[
        {'role': 'user', 'content': "今天合肥的天气怎么样？"},
    ],
    functions=functions,
    function_call="auto",
)
print(completion)

# {
#   "id": "chatcmpl-7pQtQZWjQpciRel2pikFo29aHQ0fN",
#   "object": "chat.completion",
#   "created": 1692492460,
#   "model": "gpt-3.5-turbo-0613",
#   "choices": [
#     {
#       "index": 0,
#       "message": {
#         "role": "assistant",
#         "content": null,
#         "function_call": {
#           "name": "get_current_date",
#           "arguments": "{}"
#         }
#       },
#       "finish_reason": "function_call"
#     }
#   ],
#   "usage": {
#     "prompt_tokens": 114,
#     "completion_tokens": 8,
#     "total_tokens": 122
#   }
# }

def get_current_date(args):
    import datetime
    today = datetime.date.today()
    weekday = today.weekday()
    weeekdays = ['一','二','三','四','五','六','日']
    return '今天是' + str(today) + ', ' + '星期' + weeekdays[weekday]

function_call = completion.choices[0].message.function_call
function = globals().get(function_call.name)
args = json.loads(function_call.arguments)

result = function(args)
print(result)

# 今天是2023-08-20, 星期日

completion = openai.ChatCompletion.create(
    temperature=0.7,
    model="gpt-3.5-turbo",
    messages=[
        {'role': 'user', 'content': "今天合肥的天气怎么样？"},
        {'role': 'function', 'name': 'get_current_date', 'content': "今天是2023-08-20, 星期日"},
    ],
    functions=functions,
    function_call="auto",
)
print(completion)

# {
#   "id": "chatcmpl-7pQzBBtZn7hdy8cOnWF6ljadDKgkR",
#   "object": "chat.completion",
#   "created": 1692492817,
#   "model": "gpt-3.5-turbo-0613",
#   "choices": [
#     {
#       "index": 0,
#       "message": {
#         "role": "assistant",
#         "content": null,
#         "function_call": {
#           "name": "get_weather_info",
#           "arguments": "{\n  \"city\": \"\u5408\u80a5\",\n  \"date\": \"2023-08-20\"\n}"
#         }
#       },
#       "finish_reason": "function_call"
#     }
#   ],
#   "usage": {
#     "prompt_tokens": 137,
#     "completion_tokens": 30,
#     "total_tokens": 167
#   }
# }

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

function_call = completion.choices[0].message.function_call
function = globals().get(function_call.name)
args = json.loads(function_call.arguments)

result = function(args)
print(result)

# 晴转多云，34/25℃，东南风

completion = openai.ChatCompletion.create(
    temperature=0.7,
    model="gpt-3.5-turbo",
    messages=[
        {'role': 'user', 'content': "今天合肥的天气怎么样？"},
        {'role': 'function', 'name': 'get_current_date', 'content': "今天是2023-08-20, 星期日"},
        {'role': 'function', 'name': 'get_weather_info', 'content': "晴转多云，34/25℃，东南风"},
    ],
    functions=functions,
    function_call="auto",
)
print(completion.choices[0].message.content)

# 今天合肥的天气是晴转多云，最高温度为34℃，最低温度为25℃，风向为东南风。
