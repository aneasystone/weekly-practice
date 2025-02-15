# pip install tabula-py
import tabula

dfs = tabula.read_pdf("./pdfs/3.pdf", pages='all')
print(dfs[0])
