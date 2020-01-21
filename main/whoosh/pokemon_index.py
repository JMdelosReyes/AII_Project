import os

from whoosh.fields import Schema, TEXT, DATETIME, KEYWORD, ID, NUMERIC
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser

from main.models import Pokemon

DIR_INDEX = "index"


def get_schema():
    return Schema(pokedex_id=ID(stored=True), name=TEXT(stored=True), generation=NUMERIC(stored=True),
                  primary_type=TEXT(stored=True), secondary_type=TEXT(stored=True))


def add_pokemon_doc(writer, pokemon):
    writer.add_document(pokedex_id=str(pokemon.pokedex_id), name=pokemon.name,
                        generation=pokemon.generation.gen_id,
                        primary_type=pokemon.primary_type.name,
                        secondary_type='' if pokemon.secondary_type is None else pokemon.secondary_type.name)


def create_pokemon_index():
    directory = os.path.join('main', DIR_INDEX)
    if not os.path.exists(directory):
        os.mkdir(directory)

    ix = create_in(directory, schema=get_schema())
    writer = ix.writer()
    for pokemon in Pokemon.objects.all():
        add_pokemon_doc(writer, pokemon)
    writer.commit()


def search_pokemon(primary_type, secondary_type):
    ix = open_dir(os.path.join('main', DIR_INDEX))
    pokemons = []
    with ix.searcher() as searcher:
        primary_type = '' if primary_type == '-' else primary_type

        query = primary_type
        if secondary_type != '-':
            query = query + ' secondary_type:' + secondary_type

        query = QueryParser("primary_type", ix.schema).parse(query)
        results = searcher.search(query, limit=None)
        for r in results:
            pokemons.append(Pokemon.objects.get(pokedex_id=r['pokedex_id']))
    return pokemons
