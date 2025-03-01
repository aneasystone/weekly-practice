import pikepdf

with pikepdf.open('./pdfs/example.pdf') as pdf:
    num_pages = len(pdf.pages)
    print(num_pages)
    
    page = pdf.pages[0]
    instructions = pikepdf.parse_content_stream(page)
    data = pikepdf.unparse_content_stream(instructions)
    print(data.decode())
    
    page = pdf.pages[3]
    for key in page.images:
        rawimage = page.images[key]
        pdfimage = pikepdf.PdfImage(rawimage)
        pdfimage.extract_to(fileprefix='x')