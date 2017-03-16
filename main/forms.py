from dal import autocomplete
from datetime import datetime, timedelta
from django import forms
from django.forms.widgets import RadioSelect

from .models import Teacher

class CriteriaForm(forms.Form):

    class Meta:
        model = Teacher
        fields = ('id','tName',)
    
    teachers = Teacher.objects.order_by('tName')
    '''
    #  Old, without autocomplete
    
    TEACHER_NAMES = [(t.id, '{0} {1}.{2}.'.format(
        t.tName.split(sep=' ')[0],
        t.tName.split(sep=' ')[1][0],
        t.tName.split(sep=' ')[2][0])) for t in teachers]
    
    ch_teacher = forms.ChoiceField(choices=TEACHER_NAMES,
                                   label='Преподаватель:')
    '''
    ch_teacher = forms.ModelChoiceField(
        queryset=teachers,
        label='Преподаватель:',
        widget=autocomplete.ModelSelect2(url='teacher_autocomplete'))

    date_since = forms.DateField(
        initial=datetime.now().strftime('%d.%m.%Y'),
        input_formats=['%d.%m.%Y'],
        label="Дата, с:")

    date_to = forms.DateField(
        initial=(datetime.now()+timedelta(days=7)).strftime('%d.%m.%Y'),
        input_formats=['%d.%m.%Y'],
        label="Дата, по:")

    view_method = forms.ChoiceField(
        widget=RadioSelect,
        label="Отобразить как:",
        choices=[('1', 'список'),('2', 'таблицу')],
        initial='1')
