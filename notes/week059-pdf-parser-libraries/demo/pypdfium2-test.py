# pip install -U pypdfium2
import pypdfium2 as pdfium

pdf = pdfium.PdfDocument("./pdfs/example.pdf")
for i in range(len(pdf)):
    print('----- Page %d -----' % (i+1))
    page = pdf[i]
    textpage = page.get_textpage()
    text_all = textpage.get_text_bounded()
    print(text_all)

# 读取区域
page = pdf[4]
textpage = page.get_textpage()
rect_count = textpage.count_rects()
print(rect_count)
for i in range(rect_count):
    rect = textpage.get_rect(i)
    print(rect)
    text = textpage.get_text_bounded(rect[0], rect[1], rect[2], rect[3])
    print(text)

# 读取范围
page = pdf[0]
textpage = page.get_textpage()
text = textpage.get_text_range(3, 2)
print(text)

# 搜索
searcher = textpage.search("正文")
while True:
    match = searcher.get_next()
    if match:
        print(match)
    else:
        break

# 读取图片
page = pdf[3]
for obj in page.get_objects():
    print(obj.level, obj.type, obj.get_pos())
    if isinstance(obj, pdfium.PdfImage):
        bitmap = obj.get_bitmap()
        pil_image = bitmap.to_pil()
        pil_image.save(f"x.png")

# 转换为图片
page = pdf[3]
bitmap = page.render(
    scale = 1,    # 72dpi resolution
    rotation = 0, # no additional rotation
)
pil_image = bitmap.to_pil()
pil_image.save('x.png')

# 使用 Tesseract OCR 识别文本
from PIL import Image
import pytesseract
data = pytesseract.image_to_string(Image.open("x.png"), config="--psm 6")
print(data)