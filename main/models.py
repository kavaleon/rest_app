from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

class Person(models.Model):
    """ Модель студента """
    name = models.CharField(max_length=30, verbose_name='имя')
    surname = models.CharField(max_length=30, verbose_name='фамилия')
    slug = models.SlugField(verbose_name='url', help_text='только латинские', max_length=80, db_index=True, unique=True)
    age = models.SmallIntegerField(validators=[MinValueValidator(12), MaxValueValidator(99)])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('person', kwargs={'id': self.pk})

    class Meta:
        verbose_name = 'студент'
        verbose_name_plural = 'студенты'
        unique_together = [['name', 'surname']]
        #db_table = 'student'
        ordering = ['surname']


class Course(models.Model):
    """ Модель курса """
    title = models.CharField(max_length=100, verbose_name='название курса')
    course_id = models.CharField(max_length=20, unique=True, verbose_name='id курса')  # добавил unique

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        ordering = ['title']

class Enrollment(models.Model):
    """
    Модель связи между студентами и курсами.
    """
    student = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='студент')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    def __str__(self):
        return f"{self.student} - {self.course}"

    class Meta:
        verbose_name = 'запись на курс'
        verbose_name_plural = 'записи на курсы'
        unique_together = [['student', 'course']]
        ordering = ['student']


class Grade(models.Model):
    """ Модель оценок для каждого студента по каждому курсу """

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, verbose_name='запись на курс', related_name='grades')
    grade = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='оценка'
    )
    date = models.DateField(auto_now_add=True, verbose_name='дата получения оценки')

    def __str__(self):
         return f"{self.enrollment} - Оценка: {self.grade}"

    class Meta:
        verbose_name = 'оценка'
        verbose_name_plural = 'оценки'
        ordering = ['date']
