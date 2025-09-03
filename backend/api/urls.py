from django.urls import path
from . import views

urlpatterns = [
    path('', views.getNote),
    path('add/',views.addNote),
]