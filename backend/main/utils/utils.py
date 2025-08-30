import pdfplumber
import os

def extract_text_from_pdf(file_path):
    output_dir = r"F:\Personal Project\study-buddy-mvp\backend\notes\txt"
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_dir, base_name + ".txt")

    text = ''
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            content = page.extract_text()
            if content:
                text += content + '\n'
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)

extract_text_from_pdf(r"F:\Resume - Bibek Adhikari.pdf")
