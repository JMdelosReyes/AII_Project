from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from main import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('about/', views.index, name='about'),
    path('pokemon/', views.all_pokemon, name='pokemon'),
    path('pokemon/generation/<int:gen_id>', views.all_pokemon, name='pokemon_gen'),
    path('pokemon/type/<str:type_name>', views.all_pokemon, name='pokemon_type'),
    path('generation/', views.generations, name='generations'),
    path('types/', views.pokemon_by_type, name='types'),
    path('populate/', login_required(views.populate), name='populate'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', views.index, name=''),
]
