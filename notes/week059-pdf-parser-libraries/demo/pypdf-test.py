# pip install pypdf
from pypdf import PdfReader

# reader = PdfReader("./pdfs/2.pdf")
reader = PdfReader("./pdfs/3.pdf")
# reader = PdfReader("./pdfs/2410.09871v1.pdf")
number_of_pages = len(reader.pages)
print(number_of_pages)

page = reader.pages[0]
text = page.extract_text()
print(text)
