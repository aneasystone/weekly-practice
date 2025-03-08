# pip install tabula-py
import tabula

dfs = tabula.read_pdf(
    "./pdfs/table.pdf",
    pages='1'
)
print(dfs[0])
