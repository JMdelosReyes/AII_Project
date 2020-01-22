from django.contrib import admin

from main.models import Generation, Pokemon, Type, Ability, Move, Trainer, Rating

admin.site.register(Generation)
admin.site.register(Type)
admin.site.register(Ability)
admin.site.register(Move)
admin.site.register(Pokemon)
admin.site.register(Trainer)
admin.site.register(Rating)
