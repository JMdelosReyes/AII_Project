from django.db.models import Q
from django.shortcuts import render, redirect

from main.models import Pokemon, Generation, Type
from main.populate.populate import populate_database

from main.forms import ElementalTypeForm, SearchForm
from main.whoosh.pokemon_index import create_pokemon_index, search_pokemon


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'index.html')


def populate(request):
    populate_database()
    create_pokemon_index()
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


def generations(request):
    return render(request, 'generation/generation_list.html',
                  {'generations': Generation.objects.all(), 'title': 'All generations'})


def pokemon_by_type(request):
    if request.method == 'POST':
        form = ElementalTypeForm(request.POST)
        if form.is_valid():
            elemental_type = form.cleaned_data['type']
            type_db = Type.objects.get(name=elemental_type)
            if type_db:
                return redirect('pokemon_type', type_name=elemental_type)
    else:
        form = ElementalTypeForm()

    return render(request, 'pokemon/form.html', {'title': 'Select a type!', 'form': form, 'action_url': 'types'})


def search_whoosh(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            primary_type = form.cleaned_data['primary_type']
            secondary_type = form.cleaned_data['secondary_type']
            generation = form.cleaned_data['generation']
            min_weight = form.cleaned_data['min_weight']
            pokemons = search_pokemon(primary_type, secondary_type, generation, min_weight)
            return render(request, 'pokemon/pokemon_list.html',
                          {'pokemons': pokemons, 'title': 'Search results'})
    else:
        form = SearchForm(initial={'primary_type': '3'})

    return render(request, 'pokemon/form.html', {'title': 'Search', 'form': form, 'action_url': 'search'})

# def get_pokemon(request, poke_id)
