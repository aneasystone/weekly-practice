from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")

@mcp.tool()
async def get_weather(city: str, date: str) -> str:
    """查询某个城市某个日期的天气.

    Args:
        city: 城市名称
        date: 日期，可以是具体的日期，如：yyyy-MM-dd，也可以是口语化的日期，如：今天、明天 等
    """
    return '天气晴，气温25摄氏度'

if __name__ == "__main__":
    mcp.run(transport='stdio')