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
   
# pip install pymupdf4llm
# import pymupdf4llm
# md_text = pymupdf4llm.to_markdown("./pdfs/example.pdf", write_images=True)
# print(md_text)
