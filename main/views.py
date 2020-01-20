from django.db.models import Q
from django.shortcuts import render

from main.models import Pokemon, Generation
from main.populate.populate import populate_database


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'index.html')


def populate(request):
    populate_database()
    return render(request, 'notification.html', {'message': 'Populate finished'})


def all_pokemon(request, gen_id=0, type_name=''):
    if gen_id != 0:
        generation = Generation.objects.get(gen_id=gen_id)
        pokemons = Pokemon.objects.filter(generation__gen_id=gen_id)
        title = f'Pokèmon de la {generation.name}'
        return render(request, 'pokemon/pokemon_list.html', {'pokemons': pokemons, 'title': title})

    if type_name != '':
        type_name = type_name.capitalize()
        pokemons = Pokemon.objects.filter(Q(primary_type__name=type_name) | Q(secondary_type__name=type_name))
        title = f'Pokèmon de tipo {type_name}'
        return render(request, 'pokemon/pokemon_list.html', {'pokemons': pokemons, 'title': title})

    return render(request, 'pokemon/pokemon_list.html', {'pokemons': Pokemon.objects.all(), 'title': 'All Pokèmon'})

# def get_pokemon(request, poke_id)
