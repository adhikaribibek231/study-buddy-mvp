from transformers import pipeline
import pdfplumber
import os

def extract_text_from_pdf(file_path):
    output_dir = r"F:\Personal Project\study-buddy-mvp\backend\notes\summary"
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_dir, base_name + ".txt")

    if os.path.exists(output_path):
        print(f"Skipped: '{output_path}' already exists.")
        return

    text = ''
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            content = page.extract_text()
            if content:
                text += content + '\n'
    summary = summarize(text)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(summary)
    print(f"Extracted: '{output_path}' created successfully.")


def summarize(text):
    summarizer = pipeline('summarization', model = 'facebook/bart-large-cnn')
    summary = summarizer(text, max_length = 1000, min_length=500, do_sample = False)
    return (summary[0]['summary_text'])

extract_text_from_pdf(r"G:\Compiler Design\compiler design.pdf")
