from transformers import pipeline, BartTokenizer
import pdfplumber
import os

# Initialize once
model_name = 'facebook/bart-large-cnn'
summarizer = pipeline('summarization', model=model_name, device = 0)
tokenizer = BartTokenizer.from_pretrained(model_name)

def extract_text_from_pdf(file_path):
    output_dir = r"F:\Personal Project\study-buddy-mvp\backend\notes\summary"
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_dir, base_name + ".txt")

    if os.path.exists(output_path):
        print(f"Skipped: '{output_path}' already exists.")
        return

    text = ''
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + '\n'

    summary = summarize_large_text(text)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"Extracted: '{output_path}' created successfully.")


def chunk_text_by_tokens(text, max_tokens=1024):
    """Split text into chunks based on tokenizer tokens, not words."""
    tokens = tokenizer.encode(text, add_special_tokens=False)
    for i in range(0, len(tokens), max_tokens):
        yield tokenizer.decode(tokens[i:i + max_tokens], skip_special_tokens=True)


def summarize_large_text(text):
    # First-level summaries
    chunk_summaries = []
    for chunk in chunk_text_by_tokens(text, max_tokens=1024):
        summary = summarizer(chunk, max_length=300, min_length=100, do_sample=False)
        chunk_summaries.append(summary[0]['summary_text'])

    # Second-level summary
    combined = " ".join(chunk_summaries)
    final_summary = summarizer(combined, max_length=500, min_length=200, do_sample=False)
    return final_summary[0]['summary_text']


# Run
extract_text_from_pdf(r"G:\Compiler Design\compiler design.pdf")