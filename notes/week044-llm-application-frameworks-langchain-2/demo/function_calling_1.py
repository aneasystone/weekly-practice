import os
import openai
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

completion = openai.ChatCompletion.create(
    temperature=0.7,
    model="gpt-3.5-turbo",
    messages=[
        {'role': 'user', 'content': "今天是星期几？"},
    ],
    functions=[
        {
            "name": "get_current_date",
            "description": "获取今天的日期信息，包括几月几号和星期几",
            "parameters": {
                "type": "object",
                "properties": {}
			}
        }
    ],
    function_call="auto",
)
print(completion)

# {
#   "id": "chatcmpl-7pQO7iJ3WeggIYZ5CnLc88ZxMgMMV",
#   "object": "chat.completion",
#   "created": 1692490519,
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
#     "prompt_tokens": 63,
#     "completion_tokens": 8,
#     "total_tokens": 71
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
        {'role': 'user', 'content': "今天是星期几？"},
        {'role': 'function', 'name': 'get_current_date', 'content': "今天是2023-08-20, 星期日"},
    ],
)
print(completion)

# {
#   "id": "chatcmpl-7pQklbWnMyVFvK73YbWXMybVsOTJe",
#   "object": "chat.completion",
#   "created": 1692491923,
#   "model": "gpt-3.5-turbo-0613",
#   "choices": [
#     {
#       "index": 0,
#       "message": {
#         "role": "assistant",
#         "content": "今天是星期日。"
#       },
#       "finish_reason": "stop"
#     }
#   ],
#   "usage": {
#     "prompt_tokens": 83,
#     "completion_tokens": 8,
#     "total_tokens": 91
#   }
# }
