# pip install markitdown
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("./pdfs/example.docx")
print(result.text_content)

# from openai import Client
# client = Client()
# md = MarkItDown(llm_client=client, llm_model="gpt-4o")
# result = md.convert("./pdfs/example.jpg")
# print(result.text_content)

# md = MarkItDown()
# result = md.convert("./pdfs/example.pdf")
# print(result.text_content)