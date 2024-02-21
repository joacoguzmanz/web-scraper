import os
from pdfminer.high_level import extract_text
from doc_utils import sanitize_text, save_text_to_json
import pandas as pd
from scraping import iterate_through_web, iterate_v2

# TODO function to iterate and add to JSON


if __name__ == '__main__':
    fermax_url = 'https://www.fermax.com/spain/documentacion/documentacion-tecnica'
    test_fermax_text = '/Users/joaquinguzman/Downloads/fermax-pdf-testing.pdf'
    test_fermax_excel = '/Users/joaquinguzman/Desktop/fermax/listado-de-sustitutos-y-equivalencias.xlsx'
    fermax_path_test = os.path.join(os.path.expanduser('~'), 'Desktop/fermax/')

