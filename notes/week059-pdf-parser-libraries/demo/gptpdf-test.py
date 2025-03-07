#pip install gptpdf

from gptpdf import parse_pdf

content, image_paths = parse_pdf(
    pdf_path = "./pdfs/text+image.pdf", 
    output_dir = "./out",
    model = "gpt-4o",
)
print(content)
