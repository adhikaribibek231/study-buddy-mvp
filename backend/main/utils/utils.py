from transformers import pipeline, BartTokenizer
import pdfplumber
import os

# Initialize model and tokenizer once
model_name = 'facebook/bart-large-cnn'
summarizer = pipeline('summarization', model=model_name, device=0)  # GPU
tokenizer = BartTokenizer.from_pretrained(model_name)

def extract_text_from_pdf(file_path):
    """Extract text from PDF and summarize it safely in multiple stages."""
    output_dir = r"F:\Personal Project\study-buddy-mvp\backend\notes\summary"
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_dir, base_name + ".txt")

    if os.path.exists(output_path):
        print(f"Skipped: '{output_path}' already exists.")
        return

    # Extract text from PDF
    text = ''
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + '\n'

    # Summarize text in chunks
    summarized_sections = summarize_in_chunks(text)

    # Save all section summaries to file
    with open(output_path, 'w', encoding='utf-8') as f:
        for idx, section_summary in enumerate(summarized_sections, start=1):
            f.write(f"--- Section {idx} ---\n")
            f.write(section_summary + "\n\n")
    print(f"Extracted: '{output_path}' created successfully.")

def chunk_text_by_tokens(text, max_tokens=1000):
    """Split text into chunks based on tokenizer tokens (token-safe)."""
    tokens = tokenizer.encode(text, add_special_tokens=False)
    for i in range(0, len(tokens), max_tokens):
        yield tokenizer.decode(tokens[i:i + max_tokens], skip_special_tokens=True)

def summarize_in_chunks(text):
    """
    Summarize text in multiple stages:
    - Each chunk is summarized individually.
    - Optional batch summarization for moderate-sized groups of chunks.
    - Returns a list of summaries for all chunks.
    """
    # First-level summaries (individual chunks)
    chunk_summaries = []
    for chunk in chunk_text_by_tokens(text, max_tokens=1000):
        if not chunk.strip():
            continue
        summary = summarizer(chunk, max_length=400, min_length=150, do_sample=False)
        chunk_summaries.append(summary[0]['summary_text'])

    if not chunk_summaries:
        return []

    # Optional second-level summaries (combine small batches for coherence)
    batch_summaries = []
    batch_size = 3
    for i in range(0, len(chunk_summaries), batch_size):
        combined = " ".join(chunk_summaries[i:i + batch_size])
        if not combined.strip():
            continue
        summary = summarizer(combined, max_length=500, min_length=200, do_sample=False)
        batch_summaries.append(summary[0]['summary_text'])

    # Return batch summaries; each can be written separately to the txt file
    return batch_summaries if batch_summaries else chunk_summaries

# Run the summarizer
extract_text_from_pdf(r"G:\Compiler Design\compiler design.pdf")
