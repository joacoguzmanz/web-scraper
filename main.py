from bs4 import BeautifulSoup
import requests
import os


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
    return final_set


# def download_file(url, path_to_save, file_type)


def download_pdf(pdf_url, path_to_save):
    response = requests.get(pdf_url, stream=True)
    if response.status_code == 200:
        file_name = pdf_url.split('slug=')[-1][:-8] + '.pdf'
        file_path = os.path.join(path_to_save, file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f'PDF saved to: {file_path}')
    else:
        print(f'Failed to download PDF from: {pdf_url}')


def download_excel(excel_url, path_to_save):
    response = requests.get(excel_url, stream=True)
    if response.status_code == 200:
        file_name = excel_url.split('slug=')[-1][:-8] + '.xlsx'
        file_path = os.path.join(path_to_save, file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f'Excel saved to: {file_path}')
    else:
        print(f'Failed to download Excel from: {excel_url}')


def download_zip(zip_url, path_to_save):
    response = requests.get(zip_url, stream=True)
    if response.status_code == 200:
        file_name = zip_url.split('slug=')[-1][:-8] + '.zip'
        file_path = os.path.join(path_to_save, file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f'ZIP saved to: {file_path}')
    else:
        print(f'Failed to download ZIP from: {zip_url}')


def iterate_through_web(base_url, content_type, qty_pages):
    url_first_page = f'{base_url}?type={content_type}'
    set_of_tags = set()
    if qty_pages == 0:
        a_tags_page = get_all_a_tags(url_first_page)
        set_of_tags.update(filter_by_href_and_file_type(a_tags_page))
        print(f'In {content_type}, downloaded {len(set_of_tags)} files')
    else:
        for num_of_page in range(1, qty_pages + 1):
            pagination_url = f'{url_first_page}&pg={num_of_page}'
            tags_bef = len(set_of_tags)
            set_of_tags.update(filter_by_href_and_file_type(get_all_a_tags(pagination_url)))
            tags_aft = len(set_of_tags)
            print(f'In {content_type} page {num_of_page}, downloaded {tags_aft - tags_bef} files')
    return set_of_tags


if __name__ == '__main__':
    fermax_url = 'https://www.fermax.com/spain/documentacion/documentacion-tecnica'
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop/fermax')
    links = set()

    menu_contents = [
        ['handbooks', 46],
        ['declarations_of_conformity', 25],
        ['techbooks', 2],
        ['presentations_and_courses', 0],
        ['tender_specs', 0],
        ['versiones_eq', 0]
    ]

    for menu_item in menu_contents:
        links.update(iterate_through_web(fermax_url, menu_item[0], menu_item[1]))

    print(list(links))
