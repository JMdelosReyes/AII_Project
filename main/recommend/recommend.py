import shelve

from django.contrib.auth.models import User

from main.models import Trainer, Rating, Pokemon
from random import randrange

from main.recommend.recommendations import transformPrefs, calculateSimilarItems


def delete_all():
    Rating.objects.all().delete()
    Trainer.objects.all().delete()
    for n in range(1, 10):
        User.objects.filter(username=f'user{n}').delete()


def populate_trainers():
    delete_all()
    for n in range(1, 10):
        user = User(username=f'user{n}', password='pass1234')
        user.save()
        trainer = Trainer(user=user)
        trainer.save()


def create_ratings():
    for trainer in Trainer.objects.all():
        for n in range(1, randrange(1, 890)):
            rating = randrange(1, 6)  # rating
            pokemon = Pokemon.objects.get(pokedex_id=n)
            r = Rating(trainer=trainer, pokemon=pokemon, rating=rating)
            r.save()


def load_dict():
    Prefs = {}  # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataRS.dat")
    ratings = Rating.objects.all()
    for ra in ratings:
        trainer = int(ra.trainer.id)
        pokemon_id = int(ra.pokemon.pokedex_id)
        rating = float(ra.rating)
        Prefs.setdefault(trainer, {})
        Prefs[trainer][pokemon_id] = rating
    shelf['Prefs'] = Prefs
    shelf['ItemsPrefs'] = transformPrefs(Prefs)
    shelf['SimItems'] = calculateSimilarItems(Prefs, n=10)
    shelf.close()
