from django.db import models

# Create your models here.


class UneconExcelFile(models.Model):

    fileName = models.CharField(
        max_length=250)

    pubDate = models.DateField(
        'Дата публикации на unecon.ru')

    faculty = models.CharField(
        max_length=250,
        blank=True)

    scheduleType = models.CharField(
        'Тип расписания',
        max_length=45,
        blank=True)

    scheduleForm = models.CharField(
        'Форма обучения',
        max_length=45,
        blank=True)

    scheduleYear = models.CharField(
        'Курс обучения',
        max_length=20,
        blank=True)

    parsed = models.BooleanField(
        default=False)

    def __str__(self):
        return self.fileName

    def create(self, **kwargs):
        f = self.create(
            fileName=kwargs['name'],
            pubDate=kwargs['upload_date'],
            faculty=kwargs['faculty'],
            scheduleType=kwargs['sch_type'],
            scheduleForm=kwargs['form'],
            scheduleYear=kwargs['course'],
        )
        return f

    def unecon_url(self):
        return 'http://unecon.ru/sites/default/files/' + self.fileName

    def local_path(self):
        return 'files/' + self.fileName
