from django.db.models import Q
from django.shortcuts import render, redirect

from main.models import Pokemon, Generation, Type
from main.populate.populate import populate_database

from main.forms import ElementalTypeForm


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

    return render(request, 'pokemon/types.html', {'title': 'Select a type!', 'form': form})

# def get_pokemon(request, poke_id)
