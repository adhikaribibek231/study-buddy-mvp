from transformers import pipeline, BartTokenizer
import pdfplumber
import os

# Initialize model and tokenizer once
model_name = 'facebook/bart-large-cnn'
summarizer = pipeline('summarization', model=model_name, device=0)  # GPU
tokenizer = BartTokenizer.from_pretrained(model_name)

def extract_text_from_pdf(file_path):
    """Extract text from PDF and summarize it."""
    output_dir = r"F:\Personal Project\study-buddy-mvp\backend\notes\summary"
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_dir, base_name + ".txt")

    if os.path.exists(output_path):
        print(f"Skipped: '{output_path}' already exists.")
        return

    # Extract text
    text = ''
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + '\n'

    # Summarize
    summary = summarize_large_text(text)

    # Save summary
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"Extracted: '{output_path}' created successfully.")

def chunk_text_by_tokens(text, max_tokens=600):
    """Split text into token-safe chunks for the model."""
    tokens = tokenizer.encode(text, add_special_tokens=False)
    for i in range(0, len(tokens), max_tokens):
        yield tokenizer.decode(tokens[i:i + max_tokens], skip_special_tokens=True)

def summarize_large_text(text):
    """Summarize large text safely in multiple stages."""
    chunk_summaries = []

    # First-level summaries (small chunks)
    for chunk in chunk_text_by_tokens(text, max_tokens=600):
        if not chunk.strip():
            continue
        summary = summarizer(chunk, max_length=200, min_length=50, do_sample=False)
        chunk_summaries.append(summary[0]['summary_text'])

    if not chunk_summaries:
        return ""

    # Second-level summaries in batches
    final_summaries = []
    batch_size = 3
    for i in range(0, len(chunk_summaries), batch_size):
        combined = " ".join(chunk_summaries[i:i + batch_size])
        if not combined.strip():
            continue
        summary = summarizer(combined, max_length=200, min_length=50, do_sample=False)
        final_summaries.append(summary[0]['summary_text'])

    if not final_summaries:
        return ""

    # Final summary, split if too long
    combined_final = " ".join(final_summaries)
    final_chunks = []
    for sub_chunk in chunk_text_by_tokens(combined_final, max_tokens=600):
        if not sub_chunk.strip():
            continue
        summary = summarizer(sub_chunk, max_length=300, min_length=100, do_sample=False)
        final_chunks.append(summary[0]['summary_text'])

    combined_final = " ".join(final_chunks)

    # Final summary output
    final_summary = summarizer(combined_final, max_length=500, min_length=200, do_sample=False)
    return final_summary[0]['summary_text']

# Run the summarizer
extract_text_from_pdf(r"G:\Compiler Design\compiler design.pdf")
