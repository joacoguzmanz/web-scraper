import os
from doc_utils import clean_json

if __name__ == '__main__':
    fermax_path = os.path.join(os.path.expanduser('~'), 'Desktop/fermax/')
    fermax_json = os.path.join(os.path.expanduser('~'), 'Desktop/fermax/0-output/fermax-data.json')

    clean_json(fermax_json)
