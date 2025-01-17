from bs4 import BeautifulSoup

from main.models import Type
from main.populate.populate_utils import open_url, WIKI_URL

TYPES_URL = f'{WIKI_URL}/Tipos_elementales'


def extract_types_data():
    raw_data = open_url(TYPES_URL)
    if raw_data:
        soup = BeautifulSoup(raw_data, 'html.parser')
        types_soup = soup.find('table').find_all('tr')[1:]

        types = []
        cont = 1
        for t in types_soup:
            type_id = cont
            name = t.find('td').text.strip()
            cont = cont + 1

            try:
                types.append(Type(int(type_id), name))
            except Exception as e:
                print(e)
                print(
                    f'----------Error---------- : ID: {type_id} - Name: {name}')

        return types


def populate_types():
    Type.objects.bulk_create(extract_types_data())
    print(f'Types inserted: {Type.objects.count()} - Expected: 19')
