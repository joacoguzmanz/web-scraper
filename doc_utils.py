import tiktoken
import json
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


def save_text_to_json(text_to_save, json_path):
    data = {}
    for num, text in enumerate(text_to_save):
        data[f"doc_{num}"] = {
            "title": f"fermax-{num}",
            "content": text,
            "tokens": str(get_tokens_qty(text))
        }
    # Open the file in write mode and save the data as JSON
    with open(json_path, "w") as json_file:
        json.dump(data, json_file)
