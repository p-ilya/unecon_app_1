from django.db import models

# Create your models here.
class Faculty(models.Model):
    fFullName = models.CharField('Полное название',
                                 max_length=250)
    fShortName = models.CharField('Сокращенное название',
                                  max_length=45)

    def __str__(self):
        return self.fShortName
    def __repr__(self):
        return self.fFullName

class Cafedra(models.Model):
    cFaculty = models.ForeignKey(Faculty,
                                 verbose_name='Факультет')
    cFullName = models.CharField('Полное название',
                                 max_length=250)
    cShortName = models.CharField('Аббревиатура',
                                  max_length=45)

    def __str__(self):
        return self.cFullName

class Group(models.Model):
    idGroup = models.CharField('Название группы',
                               max_length=45,
                               primary_key=True)
    yearOfBegin = models.DateField('Год начала обучения')
    gFaculty = models.ForeignKey(Faculty,
                                 verbose_name='Факультет')

    def __str__(self):
        return self.idGroup

class Teacher(models.Model):
    tName = models.CharField('ФИО преподавателя',
                             max_length=100)
    tCafedra = models.ForeignKey(Cafedra,
                                 verbose_name='Кафедра')
    tEmail = models.EmailField('E-mail',
                               blank=True)

    def __str__(self):
        return self.tName

class Lesson(models.Model):
    lDate = models.DateField(auto_now=False)
    lName = models.CharField(max_length=250)
    lTeacher = models.ForeignKey(Teacher)
    lGroup = models.ForeignKey(Group)
    lTime = models.CharField(max_length=45)
    lAud = models.CharField('Аудитория',
                            max_length=45)
    lComment = models.TextField()

    def __str__(self):
        return ('{0} {1}, {2}'.format(self.lDate,
                                      self.lTime,
                                      self.lTeacher))


    
