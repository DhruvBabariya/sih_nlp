from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('',views.projects,name='index'),
   path('create/',views.createproject,name='createproject'),
   path('project/<int:pk>/chart',views.projectchart,name='projectchart'),
   path('project/<int:pk>/detail',views.projectdetail,name='projectdetail'),
   path('single_review',views.single_review,name='single_review'),
   path('project/<int:pk>/context',views.projectcontext,name='projectcontext'),
]