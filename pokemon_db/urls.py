from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from main import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('pokemon/', views.all_pokemon, name='pokemon'),
    path('pokemon/generation/<int:gen_id>', views.all_pokemon, name='pokemon_gen'),
    path('pokemon/type/<str:type_name>', views.all_pokemon, name='pokemon_type'),
    path('pokemon/highest/', views.highest_pokemon, name='highest'),
    path('generation/', views.generations, name='generations'),
    path('types/', views.pokemon_by_type, name='types'),
    path('search/', views.search_whoosh, name='search'),
    path('pokemon/<int:poke_id>', views.pokemon_view, name='pokemon_view'),
    path('move/', views.all_moves, name='moves'),
    path('move/type/<str:type_name>', views.all_moves, name='moves_type'),
    path('move/type/', views.moves_by_type, name='move_types'),
    path('move/strongest/', views.strongest_moves, name='strongest'),
    path('populate/', login_required(views.populate), name='populate'),
    path('recommend/', login_required(views.recommend), name='recommend'),
    path('recommend/pokemon/', login_required(views.similar_pokemon), name='recommend_pokemon'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', views.index, name=''),
]
