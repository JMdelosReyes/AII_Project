from django.contrib import admin

from main.models import Generation, Pokemon, Type, Ability

admin.site.register(Generation)
admin.site.register(Type)
admin.site.register(Ability)
admin.site.register(Pokemon)
