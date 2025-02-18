from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Equipment Home Page")

# Create your views here.
