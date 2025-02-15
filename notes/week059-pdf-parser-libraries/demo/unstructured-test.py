# pip install "unstructured[all-docs]"
from unstructured.partition.auto import partition

# elements = partition(filename="./pdfs/1.pdf")
# elements = partition(filename="./pdfs/2.pdf")
# elements = partition(filename="./pdfs/3.pdf")
elements = partition(filename="./pdfs/4.pdf")
# elements = partition(filename="./pdfs/2410.09871v1.pdf")
print("\n\n".join([str(el) for el in elements]))

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
#   >>> nltk.download('punkt_tab')
#   
#   For more information see: https://www.nltk.org/data.html
# 
#   Attempted to load tokenizers/punkt_tab/english/
#