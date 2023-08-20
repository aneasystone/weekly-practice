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
        completion = openai.ChatCompletion.create(
            temperature=0.7,
            model="gpt-3.5-turbo",
            messages=messages,
            functions=functions,
            function_call="auto",
        )
        # print(completion)
        message = completion.choices[0].message
        if 'function_call' not in message:
            break

        # do function calling
        function_call = message.function_call
        function = globals().get(function_call.name)
        args = json.loads(function_call.arguments)
        result = function(args)
        # print(result)
        messages.append(
            {'role': 'function', 'name': function_call.name, 'content': result},
        )
    return completion

completion = chat_completion_with_function_calling('今天是几号？')
print(completion.choices[0].message.content)
# 今天是2023年8月20日，星期日。

completion = chat_completion_with_function_calling('昨天是星期几？')
print(completion.choices[0].message.content)
# 昨天是星期六。

completion = chat_completion_with_function_calling('明天合肥的天气怎么样？')
print(completion.choices[0].message.content)
# 明天合肥的天气预报为雷阵雨，最高温度为33℃，最低温度为24℃，风向将从北风转为西北风。请注意防雷阵雨的天气情况。

completion = chat_completion_with_function_calling('昨天合肥的天气怎么样？')
print(completion.choices[0].message.content)
# 很抱歉，我无法查询到昨天合肥的天气信息。
