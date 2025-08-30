import pdfplumber

def extract_text_from_pdf(file_path):
    text =''
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            content = page.extract_text()
            if content:
                text+=content + '\n'
            
    return text

filename = r"F:\Personal Project\study-buddy-mvp\backend\notes\txt\resume.txt"
with open(filename, 'w', encoding='utf-8') as file:
    file.write(extract_text_from_pdf("F:\Resume - Bibek Adhikari.pdf"))
