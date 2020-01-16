from bs4 import BeautifulSoup

from main.models import Ability
from main.populate.populate_utils import open_url, BASE_URL

ABILITIES_URL = f'{BASE_URL}/Lista_de_habilidades'


def extract_abilities_data():
    raw_data = open_url(ABILITIES_URL)
    if raw_data:
        soup = BeautifulSoup(raw_data, 'html.parser')
        abilities_tables = soup.find_all('table')

        abilities_soup = []
        for t in abilities_tables:
            abilities_soup = abilities_soup + t.find_all('tr')[2:]

        abilities = []
        cont = 1
        for a in abilities_soup:
            td = a.find_all('td')
            ability_id = cont
            spanish_name = td[1].find('a').text.strip()
            english_name = td[1].find('i').text.strip()
            description = td[2].text.strip()
            cont = cont + 1

            # print(f'ID: {ability_id} - Spanish name: {spanish_name} - English name: {english_name}'
            #       f' - Description: {description}')

            try:
                abilities.append(Ability(int(ability_id), spanish_name, english_name, description))
            except:
                print(
                    f'----------Error---------- : ID: {ability_id} - Name: {spanish_name}')

        return abilities


def populate_abilities():
    Ability.objects.bulk_create(extract_abilities_data())
    print(f'Abilities inserted: {Ability.objects.count()} - Expected: 258')
