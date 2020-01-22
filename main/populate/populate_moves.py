from bs4 import BeautifulSoup

from main.models import Move, Type
from main.populate.populate_utils import open_url, BASE_URL, WIKI_URL

MOVES_URL = f'{WIKI_URL}/Lista_de_movimientos'


def extract_move(move_tr, move_id):
    line_tds = move_tr.find_all('td')
    link = line_tds[0].find('a')['href']

    raw_data = open_url(f'{BASE_URL}{link}')
    if raw_data:
        try:
            soup = BeautifulSoup(raw_data, 'html.parser')
            table = soup.find('div', class_='ctipo')

            spanish_name = table.find('div', class_='titulo').text.strip()
            english_name = table.find('div', class_='rboxint').find('div', class_='vnav_datos').find('table').find(
                'tr').find('td').text.strip()
            type_name = table.find('div', class_='combate').find('td').find('a').get('title').strip().split(' ')[
                1].capitalize()
            type_db = Type.objects.get(name=type_name)
            cat = \
                table.find('div', class_='combate').find_all('tr')[1].find('td').find('a').get('title').strip().split(
                    ' ')[
                    1]
            if cat == 'estado':
                category = 'Status'
            elif cat == 'especial':
                category = 'Special'
            else:
                category = 'Physical'

            power = table.find('div', class_='combate').find_all('tr')[2].find('td').text.strip()
            if power.startswith('-'):
                power = None

            accuracy = table.find('div', class_='combate').find_all('tr')[3].find('td').text.strip()
            if accuracy == '-':
                accuracy = None

            power_points = table.find('div', class_='combate').find_all('tr')[4].find('td').text.strip().split('(')
            min_power_points = power_points[0].strip()
            max_power_points = power_points[1].split(')')[0].strip()
            secondary_effect = table.find('div', class_='combate').find_all('tr')[6].find('td').text.strip()
            priority = table.find('div', class_='combate').find_all('tr')[7].find('td').text.strip().split('(')[0]
            contact = table.find('div', class_='combate').find_all('tr')[8].find('td').text.strip()
            if contact == 'Sí':
                contact_bool = True
            else:
                contact_bool = False

            magic_coat = table.find('div', class_='afectado').find_all('tr')[0].find('td').text.strip()
            if magic_coat == 'Sí':
                magic_coat_affected = True
            else:
                magic_coat_affected = False

            protection = table.find('div', class_='afectado').find_all('tr')[1].find('td').text.strip()
            if protection == 'Sí':
                protection_affected = True
            else:
                protection_affected = False

            snatch = table.find('div', class_='afectado').find_all('tr')[2].find('td').text.strip()
            if snatch == 'Sí':
                snatch_affected = True
            else:
                snatch_affected = False

            kings_rock = table.find('div', class_='afectado').find_all('tr')[3].find('td').text.strip()
            if kings_rock == 'Sí':
                kings_rock_affected = True
            else:
                kings_rock_affected = False

            try:
                m = Move(move_id, spanish_name, english_name, type_db.type_id, category, power, accuracy,
                         secondary_effect,
                         min_power_points, max_power_points, priority, contact_bool, magic_coat_affected,
                         protection_affected, snatch_affected, kings_rock_affected)
                m.save()
            except Exception as e:
                print(e)
                print(
                    f'----------Error---------- : ID: {move_id} - Name: {spanish_name}')
        except Exception as e:
            print(e)
            print(f'ERROR -------------- {BASE_URL}{link}')


def extract_moves_data():
    raw_data = open_url(MOVES_URL)
    if raw_data:
        soup = BeautifulSoup(raw_data, 'html.parser')
        moves_tables = soup.find_all('table')[1:]

        moves_soup = []
        for t in moves_tables:
            moves_soup = moves_soup + t.find_all('tr')[1:]

        cont = 1
        for move_tr in moves_soup:
            extract_move(move_tr, cont)
            cont = cont + 1


def populate_moves():
    extract_moves_data()
    print(f'Moves inserted: {Move.objects.count()} - Expected: 723')
