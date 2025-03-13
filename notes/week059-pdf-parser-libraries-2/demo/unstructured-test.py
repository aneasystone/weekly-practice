# pip install "unstructured[all-docs]"
from unstructured.partition.pdf import partition_pdf

# elements = partition_pdf(filename="./pdfs/example.pdf")
# for el in elements:
#     print(el.to_dict())

# elements = partition_pdf(filename="./pdfs/example.pdf", strategy="fast")
# for el in elements:
#     print(el.to_dict())

elements = partition_pdf("./pdfs/example.pdf", strategy="hi_res")
for el in elements:
    print(el.to_dict())

# elements = partition_pdf("./pdfs/example.pdf", strategy="ocr_only", ocr_languages="chi_sim")
# for el in elements:
#     print(el.to_dict())

from unstructured.partition.image import partition_image

# elements = partition_image("./pdfs/example.jpg", strategy="hi_res", hi_res_model_name="yolox")
# for el in elements:
#     print(el.to_dict())
    
# elements = partition_image("./pdfs/example.jpg", strategy="hi_res", hi_res_model_name="detectron2_onnx")
# for el in elements:
#     print(el.to_dict())

# --------------------------------------------------------------------

#
# ImportError: libGL.so.1: cannot open shared object file: No such file or directory
#
#  $ sudo apt update 
#  $ sudo apt install libgl1
#

#
# pdf2image.exceptions.PDFInfoNotInstalledError: Unable to get page count. Is poppler installed and in PATH?
#
#  $ sudo apt install poppler-utils
#

#
# unstructured_pytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your PATH. See README file for more information.
# 
#  $ sudo apt install tesseract-ocr
#

#
# LookupError: 
# **********************************************************************
#   Resource punkt_tab not found.
#   Please use the NLTK Downloader to obtain the resource:
# 
#   >>> import nltk
#   >>> nltk.set_proxy('http://192.168.1.37:7890')
#   >>> nltk.download('punkt_tab')
#   >>> nltk.download('averaged_perceptron_tagger_eng')
#   
#   For more information see: https://www.nltk.org/data.html
# 
#   Attempted to load tokenizers/punkt_tab/english/
#