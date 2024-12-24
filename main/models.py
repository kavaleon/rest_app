from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

class Person(models.Model):
    name = models.CharField(max_length=30, verbose_name='имя')
    surname = models.CharField(max_length=30, verbose_name='фамилия')
    slug = models.SlugField(verbose_name='url', help_text='только латинские', max_length=80, db_index=True, unique=True)
    age = models.SmallIntegerField(validators=[MinValueValidator(12), MaxValueValidator(99)])
    age2 = models.SmallIntegerField(null=True)

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
