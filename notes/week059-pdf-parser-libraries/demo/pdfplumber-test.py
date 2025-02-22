# pip install pdfplumber
import pdfplumber

path = "./pdfs/example.pdf"
with pdfplumber.open(path) as pdf:
    for i in range(len(pdf.pages)):
        print('----- Page %d -----' % (i+1))
        page = pdf.pages[i]
        text = page.extract_text()
        print(text)
        
    page = pdf.pages[2]
    tables = page.extract_tables()
    for table in tables:
        print(table)
        
        import pandas as pd
        df = pd.DataFrame(table[1:], columns=table[0])
        print(df)
        
    # page = pdf.pages[1]
    # for char in page.chars:
    #     print(char['text'], char['fontname'], char['size'], char['x0'], char['y0'], char['x1'], char['y1'])
    
    page = pdf.pages[2]
    im = page.to_image()
    im.draw_rects(page.extract_words()).save('extract_words.png')

    im = page.to_image()
    im.debug_tablefinder(table_settings={}).save('debug_tablefinder.png')
    
laparams = {
    "line_overlap": 0.5,
    "char_margin": 2.0,
    "line_margin": 0.5,
    "word_margin": 0.1,
}
with pdfplumber.open(path, laparams=laparams) as pdf:
    pass


with pdfplumber.open(path, laparams=laparams) as pdf:
    page = pdf.pages[2]
    table_settings = {
        "vertical_strategy": "lines",
        "horizontal_strategy": "lines",
        "snap_tolerance": 3,
        "join_tolerance": 3
    }
    tables = page.extract_tables(table_settings=table_settings)
    for table in tables:
        print(table)