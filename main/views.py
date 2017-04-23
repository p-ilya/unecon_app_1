from dal import autocomplete
from datetime import datetime
from django.shortcuts import render, redirect
from .forms import CriteriaForm
from .models import Lesson, Teacher

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
            lessons = Lesson.objects.filter(lTeacher_id=teacher,lDate__range=(since,to)).order_by('lDate', 'lTime')
            
            #  отладка
            #print(teacher)
            #print('{0} - {1}'.format(since, to))
            #print('METHOD '+method)
            #print(lessons)
            
            return render(request, 'main/rasp.html', {'form': form,
                                                      'lessons': lessons,
                                                      'method': method,})
    else:        
        form = CriteriaForm()
    return render(request, 'main/rasp.html', {'form': form })

def info(request):
    return render(request, 'main/info.html', {})

def show_rasp(request,since,to,teacher,method):
    # add method argument here
    lessons = Lesson.objects.filter(lTeacher=teacher,lDate__range=(since,to)).order_by('lDate', 'lTime')
    d_since = datetime.strptime(since, "%Y-%m-%d")
    d_to = datetime.strptime(to, "%Y-%m-%d")
    t = Teacher.objects.get(pk=teacher)
    t_format ='{0} {1}.{2}.'.format(
        t.tName.split(sep=' ')[0],
        t.tName.split(sep=' ')[1][0],
        t.tName.split(sep=' ')[2][0])

    return render(request, 'main/show_rasp.html', {'lessons': lessons,'method': method, 'since': d_since, 'to': d_to,'t':t_format })

class TeacherAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Teacher.objects.all()

        if self.q:
            qs = qs.filter(tName__istartswith=self.q)

        return qs