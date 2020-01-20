from django.core.validators import MinValueValidator
from django.db import models


class Pokemon(models.Model):
    pokedex_id = models.IntegerField(primary_key=True)
    # pokedex_desc = models.TextField()
    name = models.CharField(max_length=50, unique=True)
    image = models.CharField(max_length=150)
    generation = models.ForeignKey('Generation', null=True, on_delete=models.SET_NULL)
    primary_type = models.ForeignKey('Type', null=True, on_delete=models.SET_NULL, related_name="primary_type")
    secondary_type = models.ForeignKey('Type', null=True, on_delete=models.SET_NULL, related_name="secondary_type")
    abilities = models.ManyToManyField('Ability', related_name="abilities")
    hidden_ability = models.ForeignKey('Ability', null=True, on_delete=models.SET_NULL, related_name="hidden_ability")
    # evolution
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

    def __str__(self):
        return f'ID: {self.type_id} - Name: {self.name}'


class Ability(models.Model):
    ability_id = models.IntegerField(primary_key=True)
    spanish_name = models.CharField(max_length=50, unique=True)
    english_name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return f'ID: {self.ability_id} - Spanish name: {self.spanish_name} - English name: {self.english_name}'


# No Z moves
class Move(models.Model):
    move_id = models.IntegerField(primary_key=True)
    spanish_name = models.CharField(max_length=50, unique=True)
    english_name = models.CharField(max_length=50, unique=True)
    type = models.ForeignKey(Type, null=True, on_delete=models.SET_NULL)
    category = models.CharField(max_length=10,
                                choices=(('Physical', 'Physical'), ('Special', 'Special'), ('Status', 'Status')))
    power = models.PositiveIntegerField(null=True)
    accuracy = models.IntegerField(null=True, default=100)
    secondary_effect = models.CharField(max_length=100)
    min_power_points = models.PositiveIntegerField()
    max_power_points = models.PositiveIntegerField()
    priority = models.IntegerField(validators=[MinValueValidator(0)])
    contact = models.BooleanField()
    magic_coat_affected = models.BooleanField()
    snatch_affected = models.BooleanField()
    protect_affected = models.BooleanField()
    kings_rock_affected = models.BooleanField()

    def __str__(self):
        return f'ID: {self.move_id} - Spanish name: {self.spanish_name} - English name: {self.english_name}'

# class MoveLearned(models.Model):
