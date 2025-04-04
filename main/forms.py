from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework.response import Response

from .models import Course, Person
from .serializers import PersonSerializer2


class CourseAddForm(forms.Form):
    title = forms.ChoiceField(choices=[('py', 'Python'), ('js', 'Java Script'), ('c#', 'C Sharp')],
                              label='Название курса', required=True)
    course_id = forms.IntegerField(min_value=1, max_value=100, required=True)
    start_data = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'date1'}))
    end_data = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'date1'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

class TeachersAddForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"


class CourseAddForm2(forms.ModelForm):
    start_data = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'date1'}))
    class Meta:
        model = Course
        fields = "__all__"
        widgets = {
            'end_data': forms.SelectDateWidget()
        }

class PersonAddForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"
        #fields = ['name', 'surname', '...']

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 66 or age > 12:
            return age
        raise ValidationError('Возраст не подходит')



class UserRegistrationForm(forms.Form):
    '''кастомная форма для регистрации'''
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=150, required=False)
    age = forms.IntegerField(validators=[MinValueValidator(12), MaxValueValidator(99)], required=False)
    image = forms.ImageField(required=False)
    course = forms.ModelMultipleChoiceField(queryset=Course.objects.all(), required=False)
    role = forms.ChoiceField(choices=(("1", "Учитель"), ("2", "Ученик")))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not username or not password:
            raise forms.ValidationError("Username and password are required.")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return cleaned_data


class CustomLoginForm(AuthenticationForm):
    '''кастомная форма для логинирования'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})



class RegisterUserForm2(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = '__all__'


class GradeForm(forms.Form):
    student = forms.IntegerField(required=True, widget=forms.HiddenInput)
    course = forms.IntegerField(required=True, widget=forms.HiddenInput)
    grade = forms.IntegerField(required=True, widget=forms.NumberInput)