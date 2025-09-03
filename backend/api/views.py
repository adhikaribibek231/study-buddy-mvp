from rest_framework.response import Response
from rest_framework.decorators import api_view
from main.models import Note
from .serializers import NoteSerializer

@api_view(['GET'])
def getNote(request):
    items = Note.objects.all()
    serializer = NoteSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addNote(request):
    serializer = NoteSerializer(data= request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = 201)
    return Response(serializer.errors,status=400)