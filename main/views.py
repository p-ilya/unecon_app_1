from django.shortcuts import render
from .forms import CriteriaForm

# Create your views here.
def index(request):
    return render(request, 'main/index.html', {})

def rasp(request):
    form = CriteriaForm()
    return render(request, 'main/rasp.html', {'form': form })

def info(request):
    return render(request, 'main/info.html', {})

def show_rasp(request):
    # add method argument here
    return render(request, 'main/show_rasp.html', {})
