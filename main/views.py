from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'main/index.html', {})

def rasp(request):
    return render(request, 'main/rasp.html', {})

def info(request):
    return render(request, 'main/info.html', {})
