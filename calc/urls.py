from django.urls import path
from . import views

urlpatterns = [
    path('librarian', views.librarian, name ='librarian'),
    path('', views.home, name ='home')
]