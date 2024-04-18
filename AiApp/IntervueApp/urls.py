from django.urls import path
from IntervueApp import views

urlpatterns = [
    path('', views.index, name='index'),
]
