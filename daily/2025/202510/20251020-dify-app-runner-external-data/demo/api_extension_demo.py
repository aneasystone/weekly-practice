import json
from fastapi import FastAPI, HTTPException, Header

app = FastAPI()

@app.post("/api/weather")
async def query_weather(data: dict, authorization: str = Header(None)):
    
    # 简单鉴权
    expected_api_key = "123456"
    auth_scheme, _, api_key = authorization.partition(' ')
    if auth_scheme.lower() != "bearer" or api_key != expected_api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")

    print("接受到请求：" + json.dumps(data))
    
    point = data["point"]
    if point == "ping":
        return {
            "result": "pong"
        }
    if point == "app.external_data_tool.query":
        return handle_app_external_data_tool_query(params=data["params"])
    
    raise HTTPException(status_code=400, detail="Not implemented")

def handle_app_external_data_tool_query(params: dict):
    
    inputs = params.get("inputs")
    if inputs.get("city") == "合肥":
        return {
            "result": "天气晴，西北风，温度10-24摄氏度"
        }
    else:
        return {
            "result": "未知城市"
        }
