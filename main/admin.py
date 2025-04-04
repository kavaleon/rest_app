from django.contrib import admin
from .models import Person, Course, Grade
from django.db.models import Avg


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'age', 'average_grade')
    search_fields = ('surname', 'name')
    list_filter = ('age',)


    def average_grade(self, obj):
        result = Grade.objects.filter(student=obj).aggregate(Avg('grade', default=0))
        return result['grade__avg']

    average_grade.short_description = 'средний балл'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_id')



