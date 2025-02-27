# pip install --only-binary=pymupdf pymupdf
import pymupdf

doc = pymupdf.open("./pdfs/example.pdf")
number_of_pages = len(doc)
print('Total %d pages.' % (number_of_pages))
for i in range(number_of_pages):
    print('----- Page %d -----' % (i+1))
    page = doc[i]
    text = page.get_text()
    print(text)
    # html = page.get_text('html')
    # print(html)
    json = page.get_text('json')
    print(json)

from pprint import pprint
page = doc[2]
for t in page.find_tables():
    table = t.extract()
    pprint(table)
    
    import pandas as pd
    df = pd.DataFrame(table[1:], columns=table[0])
    print(df)

page = doc[3]
for img in page.get_images():
    xref = img[0]
    data = doc.extract_image(xref)['image']
    pix = pymupdf.Pixmap(data)
    # pix.save(str(img[0]) + '.png')
    # pix.pdfocr_save('x.pdf', language='eng')
    bytes = pix.pdfocr_tobytes()
    imgdoc = pymupdf.open("pdf", bytes)
    page = imgdoc[0]
    text = page.get_text()
    print(text)

# page = doc[3]
# textpage = page.get_textpage_ocr()
# text = textpage.extractText()
# print(text)

# page = doc[0]
# pix = page.get_pixmap(dpi=300)
# pix.save('x.png')
# pix.pdfocr_save('x.pdf', language='chi_sim')
# bytes = pix.pdfocr_tobytes(language='chi_sim')
# imgdoc = pymupdf.open("pdf", bytes)
# page = imgdoc[0]
# text = page.get_text()
# print(text)

# pip install pymupdf4llm
# import pymupdf4llm
# md_text = pymupdf4llm.to_markdown("./pdfs/example.pdf", write_images=True)
# print(md_text)
