# pip install pdfminer.six
from pdfminer.high_level import extract_text

text = extract_text("./pdfs/5.pdf")
print(text)