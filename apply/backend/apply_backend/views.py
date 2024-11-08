from django.shortcuts import render

# Create your views here.
def pinfo(request):
    return render(request,'pinfo.html')

def apply(request):
    return render(request,'apply.html')