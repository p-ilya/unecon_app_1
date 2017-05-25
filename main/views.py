from dal import autocomplete
from datetime import datetime
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from .forms import CriteriaForm, ExportForm
from .models import Lesson, Teacher


def filter_lessons(teacher, since, to):
    lessons = Lesson.objects.filter(
        lTeacher_id=teacher, lDate__range=(since, to)).order_by('lDate', 'lTime')
    return lessons

# Create your views here.


def index(request):
    return render(request, 'main/index.html', {})


def rasp(request):
    if request.method == "POST":
        form = CriteriaForm(request.POST)

        if form.is_valid():
            teacher = form.cleaned_data.get('ch_teacher')
            since = form.cleaned_data.get('date_since')
            to = form.cleaned_data.get('date_to')
            method = form.cleaned_data.get('view_method')
            lessons = filter_lessons(teacher, since, to)

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
            export = ExportForm(
                initial={'result_url': full_direct_url}, prefix="exp")
            #  отладка
            # print(teacher)
            #print('{0} - {1}'.format(since, to))
            #print('METHOD '+method)
            # print(lessons)

            context = {
                'form': form,
                'lessons': lessons,
                'method': method,
                'export': export,
            }

            return render(request, 'main/rasp.html', context)

    else:
        form = CriteriaForm()
    return render(request, 'main/rasp.html', {'form': form, })


def info(request):
    return render(request, 'main/info.html', {})


def show_rasp(request, since, to, teacher, method):
    #  Результат, доступный по прямой ссылке
    lessons = filter_lessons(teacher, since, to)
    d_since = datetime.strptime(since, "%Y-%m-%d")
    d_to = datetime.strptime(to, "%Y-%m-%d")
    t = Teacher.objects.get(pk=teacher)
    #  ФИО в формате Фамилия И.О.
    t_format = '{0} {1}.{2}.'.format(
        t.tName.split(sep=' ')[0],
        t.tName.split(sep=' ')[1][0],
        t.tName.split(sep=' ')[2][0]
    )

    export = ExportForm(prefix='exp')
    direct_url = reverse(
        'show_rasp',
        kwargs={
            'since': since,
            'to': to,
            'teacher': teacher,
            'method': method
        })
    export.fields['result_url'].initial = request.build_absolute_uri(
        direct_url)
    # print(export.as_table())

    context = {
        'lessons': lessons,
        'method': method,
        'since': d_since,
        'to': d_to,
        't': t_format,
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


def send_email(request):
    if request.method == "POST":
        addr = request.POST.get('exp-email_address', None)
        result_url = request.POST.get('exp-result_url', None)

        since, to, t_id, method = result_url.split(sep='/')[4:8]
        lessons = filter_lessons(t_id, since, to)

        d_since = datetime.strptime(since, "%Y-%m-%d")
        d_to = datetime.strptime(to, "%Y-%m-%d")

        t = Teacher.objects.get(pk=t_id)

        mail_context = {
            't': t,
            'since': d_since,
            'to': d_to,
            'method': method,
            'lessons': lessons
        }

        msg_text = render_to_string('email/email.txt', mail_context)
        msg = render_to_string('email/email.html', mail_context)
        send_mail('Расписание занятий СПбГЭУ', msg_text,
                  'unecon.schedule@yandex.ru', [addr, ], html_message=msg)

        context = {
            't': t,
            'since': d_since,
            'to': d_to,
            'addr': addr
        }
        return render(request, 'main/mail_sent.html', context)

    else:
        raise Http404('GET—запрос к служебной странице запрещен.')
