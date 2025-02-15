from unstructured.partition.pdf import partition_pdf

elements = partition_pdf("./pdfs/3.pdf")
print("\n\n".join([str(el) for el in elements]))

elements = partition_pdf("./pdfs/3.pdf", strategy="hi_res")
print("\n\n".join([str(el) for el in elements]))
