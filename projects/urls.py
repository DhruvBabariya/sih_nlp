from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('',views.projects,name='index'),
   path('create/',views.createproject,name='createproject'),
   
]