import os
from doc_utils import sanitize_text, save_text_to_json, process_files
from scraping import iterate_through_web, iterate_v2
from pdfminer.high_level import extract_text

# TODO function to iterate and add to JSON


if __name__ == '__main__':
    fermax_url = 'https://www.fermax.com/spain/documentacion/documentacion-tecnica'
    test_fermax_text = '/Users/joaquinguzman/Downloads/fermax-pdf-testing.pdf'
    test_fermax_excel = '/Users/joaquinguzman/Desktop/fermax/listado-de-sustitutos-y-equivalencias.xlsx'
    fermax_path = os.path.join(os.path.expanduser('~'), 'Desktop/fermax/')
    json_path = os.path.join(os.path.expanduser('~'), 'Desktop/fermax/0-output/fermax-data.json')

    process_files(fermax_path, json_path)
