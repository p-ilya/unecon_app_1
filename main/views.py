from dal import autocomplete
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
                                                      'method': method })
    else:        
        form = CriteriaForm()
    return render(request, 'main/rasp.html', {'form': form })

def info(request):
    return render(request, 'main/info.html', {})

def show_rasp(request,lessons):
    # add method argument here
    # lessons = Lesson.objects.filter(lTeacher=teacher,lDate__range=(since,to))
    
    return render(request, 'main/show_rasp.html', {'lessons': lessons})

class TeacherAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        ''' NOTE: right now teacher queryset 
        is exposed through public URL.
        Make a request.user.is_authenticated() check
        once the user system is done. '''
        qs = Teacher.objects.all()

        if self.q:
            qs = qs.filter(tName__istartswith=self.q)

        return qs