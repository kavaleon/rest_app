from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

class Person(models.Model):
    """ Модель студента """
    name = models.CharField(max_length=30, verbose_name='имя')
    surname = models.CharField(max_length=30, verbose_name='фамилия', null=True)
    username = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='username',
                             max_length=80, db_index=True, unique=True)
    age = models.SmallIntegerField(validators=[MinValueValidator(12), MaxValueValidator(99)], null=True)
    course = models.ManyToManyField(to='Course', blank=True, verbose_name='посещаемые курсы', related_name='persons')
    time_create = models.DateField(auto_now_add=True, verbose_name='дата создания', null=True)
    time_update = models.DateField(auto_now=True, verbose_name='дата изменения', null=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d', default='photos/user.png', null=True, blank=True)
    role = models.CharField(max_length=7, verbose_name='права', default='0')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('person', kwargs={'id': self.pk})


    class Meta:
        verbose_name = 'пользователи'
        verbose_name_plural = 'пользователь'
        #db_table = 'student'
        ordering = ['surname']


class Course(models.Model):
    """ Модель курса """
    langs = [('py', 'Python'), ('js', 'Java Script'), ('c#', 'C Sharp')]
    title = models.CharField(max_length=10, choices=langs, verbose_name='название курса')
    course_id = models.CharField(max_length=20, unique=True, verbose_name='номер курса')
    start_data = models.DateField(verbose_name='дата начала', blank=True, null=True)
    end_data = models.DateField(verbose_name='дата конца', blank=True, null=True)
    description = models.CharField(max_length=100, verbose_name='описание', blank=True)

    def __str__(self):
        return f"{self.title} - {self.course_id}"

    def get_students(self):
        return Person.objects.filter(course=self)

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        ordering = ['title']
        unique_together = [['course_id', 'title']]


class Grade(models.Model):
    """Модель оценки студента"""
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    grade = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                     verbose_name='оценка', null=True)
    time_create = models.DateField(verbose_name='дата создания')

    def __str__(self):
        return f'оценка {self.person} на курсе {self.course}'

    class Meta:
       verbose_name = 'оценка'
       verbose_name_plural = 'оценки'


