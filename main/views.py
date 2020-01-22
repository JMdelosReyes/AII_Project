import shelve

from django.db.models import Q, Avg
from django.shortcuts import render, redirect, get_object_or_404

from main.models import Pokemon, Generation, Type, Move
from main.populate.populate import populate_database

from main.forms import ElementalTypeForm, SearchForm, PokemonIdForm
from main.recommend.recommend import populate_trainers, create_ratings, load_dict
from main.recommend.recommendations import topMatches
from main.whoosh.pokemon_index import create_pokemon_index, search_pokemon


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'index.html')


def populate(request):
    populate_database()
    create_pokemon_index()
    return render(request, 'notification.html',
                  {'message1': 'Populate finished', 'message2': 'Now you can use the page!'})


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


def pokemon_view(request, poke_id=0):
    if poke_id == 0 or poke_id > 890:
        return redirect('index')

    pokemon = Pokemon.objects.get(pokedex_id=poke_id)
    average_rating = pokemon.rating_set.aggregate(Avg('rating'))['rating__avg']
    print(average_rating)
    return render(request, 'pokemon/pokemon_view.html', {'pokemon': pokemon, 'average_rating': average_rating})


def all_moves(request, type_name=''):
    if type_name != '':
        type_name = type_name.capitalize()
        moves = Move.objects.filter(type__name=type_name)
        title = f'Movimientos de tipo {type_name}'
        return render(request, 'move/move_list.html', {'moves': moves, 'title': title})

    return render(request, 'move/move_list.html', {'moves': Move.objects.all(), 'title': 'All Moves'})


def moves_by_type(request):
    if request.method == 'POST':
        form = ElementalTypeForm(request.POST)
        if form.is_valid():
            elemental_type = form.cleaned_data['type']
            type_db = Type.objects.get(name=elemental_type)
            if type_db:
                return redirect('moves_type', type_name=elemental_type)
    else:
        form = ElementalTypeForm()

    return render(request, 'move/form.html', {'title': 'Select a type!', 'form': form, 'action_url': 'move_types'})


def recommend(request):
    populate_trainers()
    create_ratings()
    load_dict()
    return render(request, 'notification.html',
                  {'message1': 'RS loaded', 'message2': 'Now you can use the recommendation system!'})


def similar_pokemon(request):
    if request.method == 'POST':
        form = PokemonIdForm(request.POST)
        if form.is_valid():
            pokemon_id = form.cleaned_data['pokemon_id']
            pokemon = get_object_or_404(Pokemon, pk=pokemon_id)
            shelf = shelve.open("dataRS.dat")
            items_prefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(items_prefs, int(pokemon_id), n=5)
            pokemons = []
            similar = []
            for re in recommended:
                pokemons.append(Pokemon.objects.get(pk=re[1]))
                similar.append(re[0])
            items = zip(pokemons, similar)
            return render(request, 'pokemon/pokemon_list.html',
                          {'pokemons': pokemons, 'title': f'Similar Pokèmon to {pokemon.name}'})
    else:
        form = PokemonIdForm()

    return render(request, 'recommend/form.html',
                  {'title': 'Select a Pokèmon ID!', 'form': form, 'action_url': 'recommend_pokemon'})


def highest_pokemon(request):
    pokemons = Pokemon.objects.order_by('-height')[:10]
    return render(request, 'pokemon/pokemon_list.html', {'pokemons': pokemons, 'title': 'Top 10 Highest Pokèmon'})


def strongest_moves(request):
    moves = Move.objects.order_by('-power')[:10]
    return render(request, 'move/move_list.html', {'moves': moves, 'title': 'Top 10 Strongest Moves'})
