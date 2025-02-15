from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer,NoteSerializer
from rest_framework.permissions import IsAuthenticated , AllowAny
from .models import Note



class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author = user)
    
    def perform_create(self,serializer):
        if serializer.is_valid():
            # we are explicitly specifying the author beacuse it is read only in our serializer
            serializer.save(author = self.request.user)
        else:
            print(serializer.errors)

class NoteDelete(generics.DestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)
    
class CreateUserView(generics.CreateAPIView):
    #check if user exists in all existing users objects
    queryset = User.objects.all()
    #tells the class what kind of object we need to accept to make a new user
    serializer_class = UserSerializer
    #who can call this view..here we allow anyone
    permission_classes = [AllowAny]

