from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from main import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('about/', views.index, name='about'),
    path('populate/', login_required(views.populate), name='populate'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', views.index, name=''),
]
