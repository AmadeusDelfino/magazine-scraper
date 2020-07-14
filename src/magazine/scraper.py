from urllib.request import urlopen
from bs4 import BeautifulSoup
from src.magazine.model import save_product_list, clear_product_list
import json
import re


def exec_scraper():
    list_of_products = __get_list_of_products()
    clear_product_list()
    save_product_list(list_of_products)


def __get_list_of_products():
    url_base = u'https://www.magazineluiza.com.br/aquecedor-eletrico/ar-e-ventilacao/s/ar/arae/brand---mondial'
    html = urlopen(url_base)

    parsed_html = BeautifulSoup(html, 'lxml')
    # css-9j990n is the ul class of the number of pages in the search
    total_of_pages = len(parsed_html \
                         .find('ul', {'class': 'css-9j990n'}) \
                         .findChildren('li', {'class': lambda x: x and x in x.split()})) - 2
    current_page = 1
    list_of_products_parsed = []
    while total_of_pages >= current_page:
        current_url = url_base + u'?page=' + current_page.__str__()
        current_html = urlopen(current_url)
        current_parsed_html = BeautifulSoup(current_html, 'lxml')
        list_of_products = current_parsed_html.find_all('a', {'name': 'linkToProduct'})

        for product in list_of_products:
            script_tag = product.findChildren('script', recursive=False)[0]
            product_infos = json.loads(script_tag.contents[0])
            product_infos['url'] = product['href']
            specific_product_html = urlopen(product_infos['url'])
            specific_product_parsed_html = BeautifulSoup(specific_product_html, 'lxml')
            product_infos['ean'] = __get_ean_code(
                specific_product_parsed_html.find_all(text=re.compile(r"\"ean\":\"(?:\d*)\"")))

            list_of_products_parsed.append(__normalize_product_info_names(product_infos))

        current_page += 1

    return list_of_products_parsed


def __get_ean_code(script):
    print(script[0].string)
    return re \
        .search(r"\"ean\":\"(?:\d*)\"", script[0].string) \
        .group(0) \
        .split(':')[1] \
        .replace("\"", "")


def __normalize_product_info_names(product_info):
    product_info['type'] = product_info['@type']
    product_info['brand']['type'] = product_info['brand']['@type']
    product_info['offers']['type'] = product_info['offers']['@type']

    return product_info


