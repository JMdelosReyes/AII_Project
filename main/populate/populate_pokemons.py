from bs4 import BeautifulSoup

from main.models import Pokemon, Type, Ability, Generation
from main.populate.populate_utils import open_url, BASE_URL, WIKI_URL
from main.whoosh.pokemon_index import create_pokemon_index

POKE_URL = f'{WIKI_URL}/Lista_de_Pokémon'


def correct_ability_name(name):
    switcher = {
        'Ojocompuesto': 'Ojo compuesto',
        'Absor. agua': 'Absorbe agua',
        'Absor. elec.': 'Absorbe electricidad',
        'Elec. estát.': 'Electricidad estática',
        'Elect. estát.': 'Electricidad estática',
        'Espír. vital': 'Espíritu vital',
        'Efec. espora': 'Efecto espora',
        'Sombratrampa': 'Sombra trampa',
        'Modo daruma': 'Modo Daruma',
    }
    return switcher.get(name, name)


def add_abilities(pokemon, ability_links):
    abilities = []
    for a in ability_links:
        ability_name = correct_ability_name(a.text.strip().rstrip('1'))
        try:
            ability = Ability.objects.get(spanish_name=ability_name)
            abilities.append(ability)
        except Exception as e:
            print(e)
            print(f'Error finding ability {ability_name} for {pokemon.name}')

        for ab in abilities:
            pokemon.abilities.add(ab)


def extract_pokemon(poke_id, name, link, type_1, type_2):
    raw_data = open_url(link)
    if raw_data:
        try:
            soup = BeautifulSoup(raw_data, 'html.parser')
            table = soup.find('div', class_='ctipo')

            image = table.find('a', class_='image').find('img').get('src')

            data_table = table.find('table', class_='datos')

            generation_name = data_table.find('tr', title='Generación en la que apareció por primera vez').find(
                'td').find(
                'a').get('title')
            generation = Generation.objects.get(name=generation_name)

            primary_type = Type.objects.all().get(name=type_1)
            secondary_type = None if type_2 is None else Type.objects.all().get(name=type_2)

            hidden_ab = '' if data_table.find('tr', title='Habilidad oculta') is None \
                else data_table.find('tr', title='Habilidad oculta').find('td').find('a').text.strip().rstrip('1')

            try:
                hidden_ability = None if hidden_ab == '' else Ability.objects.get(
                    spanish_name=correct_ability_name(hidden_ab))
            except Exception as e:
                print(e)
                print(f'Error finding hidden ability {hidden_ab}')
                hidden_ability = None

            weight = data_table.find('tr', title='Peso del Pokémon').find('td').text.strip().split(' ')[0]
            height = data_table.find('tr', title='Altura del Pokémon').find('td').text.strip().split(' ')[0]

            try:
                pokemon = Pokemon(pokedex_id=int(poke_id), name=name, image=image, generation=generation,
                                  primary_type=primary_type, secondary_type=secondary_type,
                                  hidden_ability=hidden_ability, weight=float(weight.replace(',', '.')),
                                  height=float(height.replace(',', '.')))
                pokemon.save()

                try:
                    ability_links = data_table.find('tr', title='Habilidades que puede conocer').find('td').find_all(
                        'a')[:2]
                    add_abilities(pokemon, ability_links)
                except Exception as e:
                    print(e)

            except Exception as e:
                print(e)
                print(
                    f'----------Error---------- : ID: {poke_id} - Name: {name}')

        except Exception as e:
            print(e)
            print(f'ERROR -------------- {link}')


def extract_all_pokemon_data():
    raw_data = open_url(POKE_URL)
    if raw_data:
        soup = BeautifulSoup(raw_data, 'html.parser')
        pokemon_tables = soup.find_all('table', class_='tabpokemon')

        pokemon_soup = []
        for t in pokemon_tables:
            pokemon_soup = pokemon_soup + t.find_all('tr')[1:]

        pokes = []
        for poke_tr in pokemon_soup:
            poke_cells = poke_tr.find_all('td')
            poke_id = poke_cells[0].text.strip()
            if poke_id != '???':
                link = f'{BASE_URL}{poke_cells[1].find("a").get("href")}'
                name = poke_cells[1].text.strip()
                type_1 = poke_cells[2].find('a').get('title').split(' ')[1].capitalize()
                type_2 = None if poke_cells[3].find('a') is None else poke_cells[3].find('a').get('title').split(' ')[
                    1].capitalize()
                extract_pokemon(poke_id, name, link, type_1, type_2)
            else:
                print('Pokemon not added yet')

        # return moves


def populate_pokemon():
    extract_all_pokemon_data()
    print(f'Pokemon inserted: {Pokemon.objects.count()} - Expected: 890')
    create_pokemon_index()
