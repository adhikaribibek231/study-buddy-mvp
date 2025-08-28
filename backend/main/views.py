from django.shortcuts import render, redirect
from .forms import NoteForm
from .models import Note

# Create your views here.
    
def upload_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("main:note_list")
    else:
        form =NoteForm()
    return render(request, "upload_note.html",{"form": form}) 

def note_list(request):
    notes = Note.objects.all()
    return render(request, "note_list.html", {"notes": notes})