# pip install camelot-py
# https://github.com/camelot-dev/camelot
import camelot
tables = camelot.read_pdf('./pdfs/3.pdf')
print(tables[0].df)
