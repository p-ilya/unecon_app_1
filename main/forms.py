from dal import autocomplete
from datetime import datetime, timedelta

from django import forms
from django.forms.widgets import RadioSelect, SelectDateWidget

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
        label="Дата, с:",
        #  Better for mobile devices?
        #  widget=SelectDateWidget(years=[2016,2017,2018,2019,2020,2021])
        widget=forms.TextInput(
            attrs={
            'class': 'datepicker',
        })
        )

    date_to = forms.DateField(
        initial=(datetime.now()+timedelta(days=7)).strftime('%d.%m.%Y'),
        input_formats=['%d.%m.%Y'],
        label="Дата, по:",
        widget=forms.TextInput(attrs={
            'class': 'datepicker',
        })
        )

    view_method = forms.ChoiceField(
        widget=RadioSelect,
        label="Отобразить как:",
        choices=[('1', 'список'),('2', 'таблицу')],
        initial='1')

class ExportForm(forms.Form):
    """Footer form for export features"""
    result_url = forms.URLField(
        label='Прямая ссылка:',
        required=False,)
    email_address = forms.EmailField(label='Адрес e-mail:',)