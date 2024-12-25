from django.contrib import admin
from .models import Person, Course, Grade
from django.db.models import Avg


# Register your models here.
#admin.site.register(Person)
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'age', 'average_grade')
    search_fields = ('surname', 'name')
    list_filter = ('age',)
    prepopulated_fields = {'slug': ('name', 'surname')}

    def average_grade(self, obj):
        result = Grade.objects.filter(person=obj).aggregate(Avg('grade', default=0))
        return result['grade__avg']

    average_grade.short_description = 'средний балл'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_id')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('person', 'grade', "create_date", "date")
