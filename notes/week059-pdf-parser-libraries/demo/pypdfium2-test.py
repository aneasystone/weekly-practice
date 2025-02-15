# pip install -U pypdfium2
import pypdfium2 as pdfium

pdf = pdfium.PdfDocument("./pdfs/1.pdf")
page = pdf[0]

textpage = page.get_textpage()
text_all = textpage.get_text_bounded()
print(text_all)

bitmap = page.render(
    scale = 1,    # 72dpi resolution
    rotation = 0, # no additional rotation
)
pil_image = bitmap.to_pil()
pil_image.save('x.png')
