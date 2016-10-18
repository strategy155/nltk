import os
import requests
import bs4
from transliterate import translit


def _translit_name(name, rev=True):
    return translit(name,'ru', reversed=rev)


def create_directory_if_needed(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return None


def produce_path(path,directory):
    return os.path.join(path,directory)


def get_webpage(url):
    _imported_web_page = requests.get(url)
    _imported_web_page.encoding='utf-8'
    return _imported_web_page


def make_soup_with_webpage(input_webpage, webpage_type):
    _imported_web_page_in_soup=bs4.BeautifulSoup(input_webpage, webpage_type+'.parser')
    return _imported_web_page_in_soup


def get_text(soup,tag='text'):
    text_instances =get_list_of_tags_with_specified_atributes(soup,tag)
    output_text = ''
    for occ in text_instances:
        output_text=output_text.join(occ.text)
    return output_text


def get_list_of_tags_with_specified_atributes(soup, tag_name, spec_dict={}):
    _all_spec_headers = soup.find_all(name=tag_name, attrs=spec_dict)
    return _all_spec_headers


def get_tags_with_special_attrs(webpage_url,webpage_type,tag_name, spec_dict):
    _req_page = get_webpage(webpage_url)
    _soup = make_soup_with_webpage(_req_page, webpage_type)
    _tags=get_list_of_tags_with_specified_atributes(_soup,tag_name,spec_dict)
    return _tags


def _choose_file_name_template(url,type):
    _name_of_types=NAME_OF_FILETYPES
    return _name_of_types[type](url)


def download_file(url, path='', type_of_file='simple-file'):
    local_filename = produce_path(path, _choose_file_name_template(url,type_of_file))
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename