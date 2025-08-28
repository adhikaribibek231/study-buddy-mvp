from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('upload/', views.upload_note, name='upload_note'),
    path('notes/',views.note_list, name="note_list"),
]