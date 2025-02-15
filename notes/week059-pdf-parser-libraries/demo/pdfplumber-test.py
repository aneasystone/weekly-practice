# pip install pdfplumber
import pdfplumber

# path = "./pdfs/1.pdf"
path = "./pdfs/5.pdf"
with pdfplumber.open(path) as pdf:
    first_page = pdf.pages[0]
    for c in first_page.chars:
        print(c['text'], end='')
        
    # im = first_page.to_image(resolution=150)
    # im.save('1.png')
    
    # im = first_page.to_image()
    # im.draw_rects(first_page.extract_words()).save('1.png')