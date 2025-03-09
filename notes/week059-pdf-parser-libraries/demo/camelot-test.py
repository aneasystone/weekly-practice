# pip install camelot-py
# https://github.com/camelot-dev/camelot
import camelot

tables = camelot.read_pdf(
    './pdfs/table.pdf',
    pages = "1",
    flavor = "stream"
    # flavor = "lattice", process_background=True,
    # flavor = "network"
    # flavor = "hybrid"
)
print(tables[0].df)
