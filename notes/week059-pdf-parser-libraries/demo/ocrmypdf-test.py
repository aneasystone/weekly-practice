import ocrmypdf

ocrmypdf.ocr('./pdfs/example.pdf', 'output.pdf', skip_text=True)

# ocrmypdf.ocr('./pdfs/example.pdf', 'output.pdf', force_ocr=True, language="chi_sim")
