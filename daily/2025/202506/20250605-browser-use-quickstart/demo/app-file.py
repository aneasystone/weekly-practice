from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")

import os
import anyio
from browser_use import Agent, Controller
from browser_use.agent.views import ActionResult
from browser_use.browser import BrowserSession

controller = Controller()

@controller.action('Read the file content of a file given a path')
async def read_file(path: str, available_file_paths: list[str]):
	if path not in available_file_paths:
		return ActionResult(error=f'File path {path} is not available')
	if not os.path.exists(path):
		return ActionResult(error=f'File {path} does not exist')

	async with await anyio.open_file(path, 'r') as f:
		content = await f.read()
	msg = f'File content: {content}'
	return ActionResult(extracted_content=msg, include_in_memory=True)

@controller.action('Upload file to interactive element with file path',)
async def upload_file(index: int, path: str, browser_session: BrowserSession, available_file_paths: list[str]):
	if path not in available_file_paths:
		return ActionResult(error=f'File path {path} is not available')
	if not os.path.exists(path):
		return ActionResult(error=f'File {path} does not exist')

	file_upload_dom_el = await browser_session.find_file_upload_element_by_index(index)
	if file_upload_dom_el is None:
		msg = f'No file upload element found at index {index}'
		return ActionResult(error=msg)

	file_upload_el = await browser_session.get_locate_element(file_upload_dom_el)
	if file_upload_el is None:
		msg = f'No file upload element found at index {index}'
		return ActionResult(error=msg)

	try:
		await file_upload_el.set_input_files(path)
		msg = f'Successfully uploaded file to index {index}'
		return ActionResult(extracted_content=msg, include_in_memory=True)
	except Exception as e:
		msg = f'Failed to upload file to index {index}: {str(e)}'
		return ActionResult(error=msg)

async def main():
    agent = Agent(
        # task="读取 test.md 文件中的内容",
		task="打开网页 https://kzmpmkh2zfk1ojnpxfn1.lite.vusercontent.net/ 并上传 test.md 文件",
        llm=llm,
		controller=controller,
        
        available_file_paths=["./test.md"],
		save_conversation_path="logs/conversation"
    )
    result = await agent.run()
    print(result)

import asyncio
asyncio.run(main())