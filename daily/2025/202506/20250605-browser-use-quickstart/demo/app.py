from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")

def base64_to_image(base64_string: str, output_filename: str):
    """Convert base64 string to image."""
    import base64
    import os

    if not os.path.exists(os.path.dirname(output_filename)):
        os.makedirs(os.path.dirname(output_filename))

    img_data = base64.b64decode(base64_string)
    with open(output_filename, "wb") as f:
        f.write(img_data)
    return output_filename

from browser_use import Agent
async def main():
    agent = Agent(
        task="Compare the price of gpt-4.1-mini and DeepSeek-V3",
        llm=llm,
        # save_conversation_path="logs/conversation"
    )
    result = await agent.run()
    # print(result)
    for i, screenshot in enumerate(result.screenshots()):
        base64_to_image(screenshot, f"screenshots/{i}.png")

import asyncio
asyncio.run(main())