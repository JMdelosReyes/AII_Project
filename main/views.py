from django.shortcuts import render

from main.populate.populate import populate_database


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'index.html')


def populate(request):
    populate_database()
    return render(request, 'index.html')
