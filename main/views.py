from django.shortcuts import render, redirect
from .models import Person
from django.views.generic import ListView, DetailView, CreateView, UpdateView

# Create your views here.
def index(request):
    return render(request, 'base.html')

def index3(request):
    return render(request, '1.html')

def index2(request, id):
    return render(request, '2.html', context={'id': id})

def users_list(request):
    users = Person.objects.all()
    user_fields = list(users[0].__dict__.keys())
    return render(request, 'users.html', {'users': users, 'user_fields': user_fields})

class users_list2(ListView):
    model = Person
    template_name = 'users2.html'
    context_object_name = 'users'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_fields'] = ['field1', 'field2']
        return context

    #   users/?filter=Ivan&filter2=22
    '''def get(self, request, *args, **kwargs):
        filter = request.GET.get('filter', default='')
        users = Person.objects.filter(surname__contains=filter)
        return render(request, 'users2.html', {'users': users})'''


class UserView(DetailView):
    model = Person
    template_name = 'user.html'
    context_object_name = 'user'
    #pk_url_kwarg = 'id'
    slug_url_kwarg = 'slug'