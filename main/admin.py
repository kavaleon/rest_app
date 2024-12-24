from django.contrib import admin
from .models import Person


# Register your models here.
#admin.site.register(Person)
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'age')
    search_fields = ('surname', 'name')
    list_filter = ('age',)
    prepopulated_fields = {'slug': ('name', 'surname')}