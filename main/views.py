from django.shortcuts import render, redirect
from .forms import CriteriaForm
from .models import Lesson

# Create your views here.
def index(request):
    return render(request, 'main/index.html', {})

def rasp(request):
    if request.method=="POST":
        form = CriteriaForm(request.POST)

        if form.is_valid():
            teacher = form.cleaned_data.get('ch_teacher')
            since = form.cleaned_data.get('date_since')
            to = form.cleaned_data.get('date_to')
            method = form.cleaned_data.get('view_method')
            lessons = Lesson.objects.filter(lTeacher_id=teacher,lDate__range=(since,to)).order_by('lDate')
            print(teacher)
            print('{0} - {1}'.format(since, to))
            print(method)
            print(lessons)
            return render(request, 'main/rasp.html', {'form': form, 'lessons':lessons})
    else:        
        form = CriteriaForm()
    return render(request, 'main/rasp.html', {'form': form })

def info(request):
    return render(request, 'main/info.html', {})

def show_rasp(request,lessons):
    # add method argument here
    # lessons = Lesson.objects.filter(lTeacher=teacher,lDate__range=(since,to))
    
    return render(request, 'main/show_rasp.html', {'lessons': lessons})
