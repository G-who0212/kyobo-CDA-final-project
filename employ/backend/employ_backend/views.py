import requests
from django.shortcuts import render
from django.http import Http404

# Create your views here.
def login(request):
    return render(request,'login.html')

def employ(request):
    return render(request,'employ.html')

def create(request):
    return render(request,'create.html')

def dashboard(request):
    return render(request,'dashboard.html')

def employdetail(request):
    return render(request, 'employdetail.html')