from datetime import datetime, date

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Course, Grade, Person
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CourseAddForm, CourseAddForm2, PersonAddForm, TeachersAddForm, RegisterUserForm2, \
    GradeForm, UserRegistrationForm, CustomLoginForm
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from calendar import monthrange
import re

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
import json

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

@login_required(login_url='/login/')
def index(request):
    try:
        person = Person.objects.get(username=request.user)
        courses = person.course.all()

        for course in courses:
            course.detail_url = f"/course/{course.id}/"

    except Person.DoesNotExist:
        return render(request, 'login.html')


    context = {
        'person': person,
        'courses': courses,
    }
    return render(request, 'main.html', context)

def courses_list(request):
    ''' список всех курсов '''
    courses = Course.objects.all()
    for course in courses:
        course.detail_url = f"/course/{course.id}/"
    return render(request, 'courses.html', {'courses': courses})


def course_add(request):
    ''' добавить курс '''
    if request.method == 'POST':
        form = CourseAddForm(request.POST)
        if form.is_valid():
            try:
                Course.objects.create(**form.cleaned_data)
                return redirect('home')
            except Exception as er:
                print(er)
                form.add_error(None, ['При сохранении возникли ошибки'])

    else:
        form = CourseAddForm()
    return render(request, 'add_course.html', context={'form': form})

def teachers_add(request):
    ''' добавить преподавателя '''
    if request.method == 'POST':
        form = TeachersAddForm(request.POST)
        if form.is_valid():
            try:
                Person.objects.create(**form.cleaned_data)
                return redirect('teachers')
            except Exception as er:
                print(er)
                form.add_error(None, ['При сохранении возникли ошибки'])

    else:
        form = TeachersAddForm()
    return render(request, 'add_teacher.html', context={'form': form})

def course_add2(request):
    ''' добавить курс '''
    if request.method == 'POST':
        form = CourseAddForm2(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses')
    else:
        form = CourseAddForm2()
    return render(request, 'add_course.html', context={'form': form})

#@cache_page(60*15)
@login_required(login_url='/login/')
def users_list(request):
    ''' Список пользователей, подписанных на выбранный курс '''

    search_query = request.GET.get('search', '')
    selected_course_id = request.GET.get('course', None)
    print('111111111111111111111111111111111',selected_course_id)
    sort_by = request.GET.get('sort', None)

    courses = Course.objects.all()

    if selected_course_id:
        print(selected_course_id)
        if selected_course_id != 'None' and selected_course_id != '':
            try:
                selected_course = Course.objects.get(pk=selected_course_id)
                print(selected_course, '5465657567')
                users = Person.objects.filter(course=selected_course)
            except Course.DoesNotExist:
                users = Person.objects.none()
        else:
            users = Person.objects.all()
    else:
        users = Person.objects.all()


    if search_query:
        users = users.filter(
            Q(name__icontains=search_query) | Q(surname__icontains=search_query)
        )

    if sort_by:
        users = users.order_by(sort_by)

    for user in users:
        user.detail_url = f"/user/{user.id}/"

    return render(request, 'users.html', {
        'users': users,
        'courses': courses,
        'selected_course_id': selected_course_id,
        'sort_by': sort_by,
    })

@login_required(login_url='/login/')
def teachers_list(request):
    ''' список всех пользователей '''

    search_query = request.GET.get('search', '')
    selected_course = request.GET.get('course', None)
    sort_by = request.GET.get('sort', None)

    teachers = Person.objects.all()
    courses = Course.objects.all()

    if search_query:
        teachers = teachers.filter(
            Q(name__icontains=search_query) | Q(surname__icontains=search_query)
        )

    if sort_by:
        teachers = teachers.order_by(sort_by)
    else:
        teachers = Person.objects.all()

    return render(request, 'teachers.html', {'teachers': teachers,
                                          'courses': courses,
                                          'sort_by': sort_by})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                cleaned_data = form.cleaned_data

                user = User.objects.create_user(
                    username=cleaned_data['username'],
                    password=cleaned_data['password'],
                    email=cleaned_data['email'],
                    first_name=cleaned_data['first_name'],
                    last_name=cleaned_data.get('last_name', '')
                )

                person = Person.objects.create(
                    username=user,
                    name=cleaned_data['first_name'],
                    surname=cleaned_data.get('last_name', ''),
                    age=cleaned_data.get('age'),
                    image=cleaned_data.get('image'),
                    role=cleaned_data.get('role')
                )

                course_ids = cleaned_data.get('course', [])
                print(f"Course IDs: {course_ids}")
                if course_ids:
                    person.course.set(course_ids)
            login(request, user)
            return render(request, 'main.html')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def course_grades(request, course_id):
    """
    Отображает информацию о курсе и таблицу с оценками студентов за каждый день месяца.
    """
    course = get_object_or_404(Course, pk=course_id)
    students = course.get_students()

    now = datetime.now()
    current_month = now.month
    current_year = now.year

    num_days = monthrange(current_year, current_month)[1]
    days_in_month = range(1, num_days + 1)


    if request.method == 'POST':
        for student in students:
            for day in days_in_month:
                for key, value in request.POST.items():
                    match = re.match(f'grade_{student.id}_{day}_(\d+)', key)
                    if match:
                        try:
                            grade_value = int(value)
                            if 0 <= grade_value <= 10:
                                lesson_date = date(current_year, current_month, day)

                                Grade.objects.create(person=student, course=course, time_create=lesson_date, grade=grade_value)

                            else:
                                raise ValueError("Оценка должна быть от 0 до 10")
                        except ValueError as e:
                            print(f"Ошибка валидации оценки: {e}")

    grades_data = {}
    for student in students:
        grades_data[student.id] = {}
        for day in days_in_month:
            lesson_date = date(current_year, current_month, day)
            grades = Grade.objects.filter(person=student, course=course, time_create=lesson_date)
            grades_data[student.id][day] = [grade.grade for grade in grades]

    context = {
        'course': course,
        'students': students,
        'days_in_month': days_in_month,
        'grades_data': grades_data,
        'current_month': now.strftime("%B"),
        'current_year': current_year,
    }
    return render(request, 'course_grades.html', context)


class UserView(DetailView, LoginRequiredMixin):
    model = Person
    template_name = 'user.html'
    context_object_name = 'user'
    slug_url_kwarg = 'slug'
    login_url = '/login/'


class UserView2(LoginRequiredMixin, DetailView):
    model = Person
    template_name = 'user.html'
    context_object_name = 'user'
    pk_url_kwarg = 'id'
    login_url = '/login/'
    success_url = reverse_lazy('user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['courses_with_grades'] = []
        grades = Grade.objects.filter(user=user)


        for course in user.course.all():
            course_grades = grades.filter(course=course)
            if course_grades:
                context['courses_with_grades'].append({
                    'course': course,
                    'grades': course_grades,
                })

        return context

class UserAddView(LoginRequiredMixin, CreateView):
    form_class = PersonAddForm
    template_name = 'add_user.html'
    success_url = reverse_lazy('users')
    login_url = '/login/'


class UserEditView(UpdateView):
    #form_class = PersonAddForm
    fields = '__all__'
    pk_url_kwarg = 'id'
    model = Person
    template_name = 'user_edit.html'
    success_url = reverse_lazy('users')

class UserDeleteView(DeleteView):
    model = Person
    template_name = 'user_delete.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('users')

class CourseEditView(UpdateView):
    fields = '__all__'
    pk_url_kwarg = 'id'
    model = Course
    template_name = 'course_edit.html'

    def get_success_url(self):
        return reverse('course', kwargs={'id': self.object.pk})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Неправильное имя пользователя или пароль.')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return render(request, 'login.html')

class CourseView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'course.html'
    context_object_name = 'course'
    pk_url_kwarg = 'id'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        is_teacher = False
        try:
            person = Person.objects.get(username=self.request.user)
            if person.role == '1':
                is_teacher = True
            elif person.role == '2':
                is_teacher = False
        except Person.DoesNotExist:
            is_teacher = False

        context['is_teacher'] = is_teacher

        if is_teacher:
            students = course.persons.all()
            context['students'] = students
        else:
            grades = person.grade_set.filter(course=course)
            context['grades'] = grades

        return context

@csrf_exempt
def receive_grade_data(request):
    print('come to send_mail')
    if request.method == 'POST':
        data = json.loads(request.body)
        grade = data.get('grade')
        date = data.get('date')
        course_id = data.get('course_id')
        person_id = data.get('person_id')

        # Получение пользователя по идентификатору
        user = get_object_or_404(User, id=person_id)

        # Получение электронной почты пользователя
        email = user.email

        message = MIMEMultipart('mixed')

        message['Subject'] = 'text email'
        message['From'] = 'gugushechk@gmail.com'
        message['To'] = email

        text = f'Добрый, вам была выставлена оценка {grade} за {date} число'


        message.attach(MIMEText(text, 'plain'))

        print('send_mail')
        with smtplib.SMTP('smtp.gmail.com', port=587) as server:
            server.starttls()
            server.login('gugushechk@gmail.com', 'waqg bgbb dfnu zpbk')
            server.sendmail(message["From"], message["To"], message.as_string())

        return JsonResponse({'status': 'success', 'email': email})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})