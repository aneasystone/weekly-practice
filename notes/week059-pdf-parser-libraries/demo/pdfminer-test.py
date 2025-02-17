# pip install pdfminer.six
from pdfminer.high_level import extract_text

text = extract_text("./pdfs/example.pdf")
print(text)

# -----

from io import StringIO
from pdfminer.high_level import extract_text_to_fp

output_string = StringIO()
with open("./pdfs/example.pdf", 'rb') as fin:
    extract_text_to_fp(fin, output_string)
print(output_string.getvalue().strip())

# -----

from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

output_string = StringIO()
with open("./pdfs/example.pdf", 'rb') as fin:
    extract_text_to_fp(fin, output_string, laparams=LAParams(),
                       output_type='html', codec=None)
print(output_string.getvalue().strip())

# ---

from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

output_string = StringIO()
with open("./pdfs/example.pdf", 'rb') as in_file:
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
print(output_string.getvalue())
