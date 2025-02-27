#
# apt update
# apt install tesseract-ocr
#
# Download chi_sim.traineddata from https://github.com/tesseract-ocr/tessdata to /usr/share/tesseract-ocr/5/tessdata/
#
# pip install pytesseract pillow
#
from PIL import Image

# 生成一个简单的测试图像（白底黑字）
from PIL import ImageDraw, ImageFont
image = Image.new("RGB", (200, 50), color="white")
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("./Songti.ttc", 20)
draw.text((10, 10), "你好", font=font, fill="black")
image.save("test.png")

# 识别测试图像
import pytesseract
text = pytesseract.image_to_string(Image.open("test.png"), lang='chi_sim')
print(text)
