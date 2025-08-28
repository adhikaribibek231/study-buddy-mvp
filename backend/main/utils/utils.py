import pdfplumber

def extract_text_from_pdf(file_path):
    text =''
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            content = page.extract_text()
            if content:
                text+=content + '\n'
            
    return text