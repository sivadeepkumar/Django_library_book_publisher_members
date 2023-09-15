
from library.models import *
from rest_framework import viewsets 
from django.shortcuts import render
from bookmanagement.serializers import *
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class Bookviewset(viewsets.ModelViewSet):
    queryset = Book.objects.all()  
    serializer_class = BookSerializer  
    authentication_classes = [BasicAuthentication] 
    permission_classes = [IsAuthenticated]