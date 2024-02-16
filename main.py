import io
from bs4 import BeautifulSoup
import requests
import os
from pdfminer.high_level import extract_text
import fitz  # PyMuPDF
import PIL.Image  # pillow
import tabula


# gets all a tags from a page
def get_all_a_tags(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    a_tags = soup.find_all('a')
    return a_tags


# filter all a tags by content and download link pattern
def filter_by_href_and_file_type(array_tags):
    final_set = set()
    href_pattern = '.doc-download'
    file_types = ['XLSX', 'PDF', 'ZIP', 'PPTX']
    for tag in array_tags:
        href = tag.get('href')
        text = tag.text.upper()
        if href_pattern in href and any(file_type in text for file_type in file_types):
            final_set.add(tag)
    return list(final_set)


# download file with extension
def download_file(url_download, path_to_save, type_of_file):
    response = requests.get(url_download, stream=True)
    if response.status_code == 200:
        file_name = url_download.split('slug=')[-1][:-8] + type_of_file
        file_path = os.path.join(path_to_save, file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f'{file_name} saved to: {file_path}')
    else:
        print(f'Failed to download file from: {url_download}')


# iterate through pages in web and download files
def iterate_through_web(base_url, content_type, qty_pages):
    fermax_path_dir = os.path.join(os.path.expanduser('~'), 'Desktop/fermax')
    url_first_page = f'{base_url}?type={content_type}'
    list_of_tags = []
    if qty_pages == 0:
        a_tags_page = get_all_a_tags(url_first_page)
        list_of_tags.extend(filter_by_href_and_file_type(a_tags_page))
        for tag in list_of_tags:
            file_extension = f'.{tag.getText().split()[0].lower()}'
            href = tag.get('href')
            download_file(href, fermax_path_dir, file_extension)
        print(f'In {content_type}, downloaded {len(list_of_tags)} files')
    else:
        for num_of_page in range(1, qty_pages + 1):
            pagination_url = f'{url_first_page}&pg={num_of_page}'
            tags_bef = len(list_of_tags)
            list_of_tags.extend(filter_by_href_and_file_type(get_all_a_tags(pagination_url)))
            for tag in list_of_tags:
                file_extension = f'.{tag.getText().split()[0].lower()}'
                href = tag.get('href')
                download_file(href, fermax_path_dir, file_extension)
            print(f'In {content_type} page {num_of_page}, downloaded {len(list_of_tags) - tags_bef} files')


# TODO functions for extracting data


if __name__ == '__main__':
    fermax_url = 'https://www.fermax.com/spain/documentacion/documentacion-tecnica'
    test_fermax_pdf = "/Users/joaquinguzman/Downloads/97865LECTORPROXIMIDADMINIWGREF5277V0917.pdf"

    menu_contents = [
        ['handbooks', 46],
        ['declarations_of_conformity', 25],
        ['techbooks', 2],
        ['presentations_and_courses', 0],
        ['tender_specs', 0],
        ['versiones_eq', 0]
    ]

    # extract all text
    text = extract_text(test_fermax_pdf)
    print(text)

    # extract tables as pandas
    tables = tabula.read_pdf(test_fermax_pdf, pages="all")
    print(tables)

    # extract all images
    pdf = fitz.open(test_fermax_pdf)
    counter = 1
    for i in range(len(pdf)):
        page = pdf[i]
        images = page.get_images()
        for image in images:
            base_img = pdf.extract_image(image[0])
            image_data = base_img["image"]
            img = PIL.Image.open(io.BytesIO(image_data))
            extension = base_img["ext"]
            img.save(open(f"image{counter}.{extension}", "wb"))
            counter += 1

    # download all pdfs from website
    for menu_item in menu_contents:
        iterate_through_web(fermax_url, menu_item[0], menu_item[1])
