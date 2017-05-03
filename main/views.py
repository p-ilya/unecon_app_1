from dal import autocomplete
from datetime import datetime
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from .forms import CriteriaForm, ExportForm
from .models import Lesson, Teacher

# Create your views here.
def index(request):
    return render(request, 'main/index.html', {})

def rasp(request):
    if request.method=="POST":
        export = ExportForm(request.POST)
        print(request.POST)
        form = CriteriaForm(request.POST)

        if form.is_valid():
            teacher = form.cleaned_data.get('ch_teacher')
            since = form.cleaned_data.get('date_since')
            to = form.cleaned_data.get('date_to')
            method = form.cleaned_data.get('view_method')
            lessons = Lesson.objects.filter(lTeacher_id=teacher,lDate__range=(since,to)).order_by('lDate', 'lTime')
            
            direct_url = reverse(
                'show_rasp',
                kwargs={
                    'since': datetime.strftime(since, '%Y-%m-%d'), 
                    'to': datetime.strftime(to, '%Y-%m-%d'), 
                    'teacher': teacher.id, 
                    'method': method
                }
            )
            full_direct_url = request.build_absolute_uri(direct_url)
            export = ExportForm(initial={'result_url': full_direct_url }, prefix="exp")
            #  отладка
            #print(teacher)
            #print('{0} - {1}'.format(since, to))
            #print('METHOD '+method)
            #print(lessons)

            context = {
                'form': form,
                'lessons': lessons,
                'method': method,
                'export': export,
            }

            return render(request, 'main/rasp.html', context)

        if export.is_valid():
            print(export.cleaned_data)

    else:        
        form = CriteriaForm()
    return render(request, 'main/rasp.html', {'form': form, })

def info(request):
    return render(request, 'main/info.html', {})

def show_rasp(request,since,to,teacher,method):
    #  Результат, доступный по прямой ссылке
    lessons = Lesson.objects.filter(lTeacher=teacher,lDate__range=(since,to)).order_by('lDate', 'lTime')
    d_since = datetime.strptime(since, "%Y-%m-%d")
    d_to = datetime.strptime(to, "%Y-%m-%d")
    t = Teacher.objects.get(pk=teacher)
    #  ФИО в формате Фамилия И.О.
    t_format ='{0} {1}.{2}.'.format(
        t.tName.split(sep=' ')[0],
        t.tName.split(sep=' ')[1][0],
        t.tName.split(sep=' ')[2][0]
    )
    
    export = ExportForm()
    direct_url = reverse(
        'show_rasp',
        kwargs={
            'since': since, 
            'to': to, 
            'teacher': teacher, 
            'method': method
        })
    export.fields['result_url'].initial = request.build_absolute_uri(direct_url)
    #print(export.as_table())
    
    context = {
        'lessons': lessons,
        'method': method, 
        'since': d_since, 
        'to': d_to,
        't':t_format, 
        'export': export 
    }
    return render(request, 'main/show_rasp.html', context)

# autocomplete view
class TeacherAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Teacher.objects.all()

        if self.q:
            qs = qs.filter(tName__istartswith=self.q)

        return qs

# Текстовый e-mail
def send_text_email(request, mailto):
    content = 'TEST MAIL'
    res = send_mail('Расписание занятий СПбГЭУ', content, 'unecon.schedule@yandex.ru', ['pyatinson@gmail.com',])
    return render(request, 'main/mail_sent.html', {'mailto': mailto })