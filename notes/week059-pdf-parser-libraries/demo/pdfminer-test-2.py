# pip install pdfminer.six
from pdfminer.high_level import extract_pages

for page in extract_pages("./pdfs/example.pdf"):
    for element in page:
        print(element)

# ---

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

for page in extract_pages("./pdfs/example.pdf"):
    for element in page:
        if isinstance(element, LTTextContainer):
            for text_line in element:
                for character in text_line:
                    if isinstance(character, LTChar):
                        print(character.get_text())
                        print(character.fontname)
                        print(character.size)
        else:
            print(element)
