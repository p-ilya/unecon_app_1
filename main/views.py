from dal import autocomplete
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import Http404
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .forms import CriteriaForm, ExportForm, TeacherFilterForm, TeacherEditForm
from .models import Lesson, Teacher, Cafedra


def filter_lessons(teacher, since, to):
    lessons = Lesson.objects.filter(
        lTeacher_id=teacher,
        lDate__range=(since, to)).order_by('lDate', 'lTime')
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
            # отладка
            # print(teacher)
            # print('{0} - {1}'.format(since, to))
            # print('METHOD '+method)
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

    context = {
        'lessons': lessons,
        'method': method,
        'since': d_since,
        'to': d_to,
        't': t.tNameShort,
        't_id': teacher,
        'export': export
    }
    return render(request, 'main/show_rasp.html', context)


def show_teacher(request, teacher):
    t_info = get_object_or_404(Teacher, pk=int(teacher))

    #  Список дисциплин преподавателя
    l_names = Lesson.objects.filter(
        lTeacher_id=int(teacher)
    ).order_by().values_list(
        'lName', flat=True
    ).distinct()

    #  Ближайшие 5 занятий
    lessons_soon = filter_lessons(
        int(teacher),
        datetime.now().strftime('%Y-%m-%d'),
        (datetime.now() + timedelta(days=31)).strftime('%Y-%m-%d')
    )[:5]

    context = {
        't': t_info,
        'l_names': l_names,
        'l_soon': lessons_soon
    }
    return render(request, 'main/show_teacher.html', context)


@login_required
def edit_teacher(request, teacher):
    teacher_ins = get_object_or_404(Teacher, pk=int(teacher))
    if request.method == 'POST':
        form = TeacherEditForm(request.POST, instance=teacher_ins)
        if form.is_valid():
            teacher = form.save()
            context = {
                't': teacher_ins,
            }
            return redirect('show_teacher', teacher=teacher.id)
            # return render(request, 'main/show_teacher.html', context)
    else:
        form = TeacherEditForm(instance=teacher_ins)
        context = {
            't': teacher_ins,
            'form': form
        }
    return render(request, 'main/edit_teacher.html', context)


def teacher_list(request):
    if request.method == "POST":
        form = TeacherFilterForm(request.POST)
        if form.is_valid():
            cafedra = form.cleaned_data.get('ch_cafedra')
            t_list = Teacher.objects.filter(tCafedra=cafedra.id)
            context = {
                'form': form,
                't_list': t_list
            }
            return render(request, 'main/teacher_list.html', context)
    else:
        form = TeacherFilterForm()
        t_list = Teacher.objects.all()
        context = {
            'form': form,
            't_list': t_list
        }
    return render(request, 'main/teacher_list.html', context)


def send_email(request):
    if request.method == "GET":
        raise Http404('GET—запрос к служебной странице запрещен.')

    # if request.method == "POST":
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


# autocomplete views

class TeacherAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Teacher.objects.all()

        if self.q:
            qs = qs.filter(tName__istartswith=self.q)

        return qs


class CafedraAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Cafedra.objects.all()

        if self.q:
            qs = qs.filter(cFullName__istartswith=self.q)

        return qs
