from main.models import Generation, Type, Ability, Move, Pokemon
from main.populate.populate_abilities import populate_abilities
from main.populate.populate_generations import populate_generations
from main.populate.populate_moves import populate_moves
from main.populate.populate_pokemons import populate_pokemon
from main.populate.populate_types import populate_types


def delete_data():
    Pokemon.objects.all().delete()
    Move.objects.all().delete()
    Generation.objects.all().delete()
    Type.objects.all().delete()
    Ability.objects.all().delete()


def populate_database():
    print("--------------- Started database population ---------------")
    delete_data()
    populate_generations()
    populate_types()
    populate_abilities()
    populate_moves()
    populate_pokemon()
    print("--------------- Finished database population ---------------")


if __name__ == '__main__':
    populate_database()
