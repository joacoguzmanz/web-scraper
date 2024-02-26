import os
import tiktoken
import json
from pdfminer.high_level import extract_text
# import fitz  # PyMuPDF
# import PIL.Image  # pillow
# import tabula


# clean up text
def sanitize_text(pdf_text):
    sanitized_lines = []
    for line in pdf_text.split('\n'):
        words = line.split()
        stripped_line = ' '.join(words)
        if stripped_line:
            sanitized_lines.append(stripped_line)
    sanitized_text = '\n'.join(sanitized_lines)
    return sanitized_text


# get quantity of tokens in pdf
def get_tokens_qty(text_from_pdf: str) -> int:
    encoding = tiktoken.get_encoding('cl100k_base')
    qty_tokens = len(encoding.encode(text_from_pdf))
    return qty_tokens


def save_text_to_json(text, title, tokens_qty, json_path):
    counter = 0
    data = {
        "title": title,
        "content": text,
        "tokens": str(tokens_qty)
    }
    if os.path.exists(json_path):
        counter += 1
        with open(json_path, "r+") as json_file:
            try:
                existing_data = json.load(json_file)
            except json.JSONDecodeError:
                existing_data = {}
            json_file.seek(0)
        counter = len(existing_data)
    else:
        existing_data = {}

    counter += 1
    existing_data["doc_" + str(counter)] = data

    with open(json_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=2)
    print(f"File {title} saved!")


def process_files(directory_path, json_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf'):
            text = extract_text(os.path.join(directory_path, filename))
            title = os.path.splitext(filename)[0]
            tokens = get_tokens_qty(text)
            save_text_to_json(text, title, tokens, json_path)
