# pip install --only-binary=pymupdf pymupdf
import pymupdf
from pprint import pprint

doc = pymupdf.open("./pdfs/3.pdf")
page = doc[0]
tabs = page.find_tables()
print(f"{len(tabs.tables)} found on {page}")

if tabs.tables:
   pprint(tabs[0].extract())
   
# pip install pymupdf4llm
import pymupdf4llm
md_text = pymupdf4llm.to_markdown("./pdfs/1.pdf")
print(md_text)
md_text = pymupdf4llm.to_markdown("./pdfs/2.pdf")
print(md_text)
md_text = pymupdf4llm.to_markdown("./pdfs/3.pdf")
print(md_text)
md_text = pymupdf4llm.to_markdown("./pdfs/4.pdf", write_images=False)
print(md_text)
md_text = pymupdf4llm.to_markdown("./pdfs/5.pdf")
print(md_text)