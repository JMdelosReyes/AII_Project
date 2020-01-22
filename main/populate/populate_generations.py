import re
from bs4 import BeautifulSoup

from main.models import Generation
from main.populate.populate_utils import open_url, WIKI_URL

GEN_URL = f'{WIKI_URL}/Generación_Pokémon'


def extract_generations_data():
    raw_data = open_url(GEN_URL)
    if raw_data:
        soup = BeautifulSoup(raw_data, 'html.parser')
        generations = soup.find('table', class_='tabpokemon').find_all('tr')[1:]

        gens = []
        cont = 1
        for gen in generations:
            gen_id = cont
            name = gen.find('th').text.strip()
            region = gen.find_all('td')[2].text.strip()
            find = re.compile(r"^[^(]*")
            added_pokemons = re.search(find, gen.find_all('td')[1].text.strip()).group(0).strip()
            cont = cont + 1

            try:
                gens.append(Generation(int(gen_id), name, region, int(added_pokemons)))
            except Exception as e:
                print(e)
                print(
                    f'----------Error---------- : ID: {gen_id} - Name: {name} - '
                    f'Region: {region} - Added Pokèmons: {added_pokemons}')

        return gens


def populate_generations():
    Generation.objects.bulk_create(extract_generations_data())
    print(f'Generations inserted: {Generation.objects.count()} - Expected: 8')
