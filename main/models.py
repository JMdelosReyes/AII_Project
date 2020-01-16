from django.core.validators import MinValueValidator
from django.db import models


class Pokemon(models.Model):
    pokedex_id = models.IntegerField(primary_key=True)
    pokedex_desc = models.TextField()
    name = models.CharField(max_length=50, unique=True)
    image = models.CharField(max_length=150)
    generation = models.ForeignKey('Generation', null=True, on_delete=models.SET_NULL)
    # types
    # evolution
    # abilities = models.ManyToManyField('Ability')
    # hidden_ability = models.ForeignKey('Ability', null=True, on_delete=models.SET_NULL)
    # moves
    weight = models.FloatField(validators=[MinValueValidator(0)])  # kg
    height = models.FloatField(validators=[MinValueValidator(0)])  # m

    def __str__(self):
        return f'ID: {self.pokedex_id} - Name: {self.name}'


class Generation(models.Model):
    gen_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    region = models.CharField(max_length=50, unique=True)
    added_pokemons = models.PositiveIntegerField()

    def __str__(self):
        return f'ID: {self.gen_id} - Name: {self.name} - Region: {self.region}'


class Type(models.Model):
    type_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)

# class Ability(models.Model):


# class Move(models.Model):


# class MoveLearned(models.Model):
