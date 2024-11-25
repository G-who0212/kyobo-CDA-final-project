from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError


# Create your views here.
def pinfo(request):
    return render(request, 'pinfo.html')

def apply(request):
    return render(request,'apply.html')