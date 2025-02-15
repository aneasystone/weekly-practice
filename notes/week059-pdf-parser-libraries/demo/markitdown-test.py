# pip install markitdown
from markitdown import MarkItDown

md = MarkItDown()
# result = md.convert("./pdfs/2.pdf")
# result = md.convert("./pdfs/3.pdf")
result = md.convert("./pdfs/4.pdf")
# result = md.convert("./pdfs/2410.09871v1.pdf")
print(result.text_content)
