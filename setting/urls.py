"""
URL configuration for setting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

import setting.settings
from main import views
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),

    path('users/', views.users_list, name='users'),
    #path('user/<int:id>/', cache_page(15*60)(views.UserView2.as_view()), name='user'),
    path('user/<int:id>/', views.UserView2.as_view(), name='user'),
    path('user/<int:id>/edit/', views.UserEditView.as_view(), name='user_edit'),
    path('user/<slug:slug>/', views.UserView.as_view()),
    path('users/add/', views.UserAddView.as_view(), name="user_add"),
    path('user/<int:id>/delete/', views.UserDeleteView.as_view(), name="user_delete"),

    path('api/', include('main.urls_rest')),


    path('teachers/add/', views.teachers_add, name='teachers_add'),


    path('courses/', views.courses_list, name='courses'),
    path('course/<int:id>/', views.CourseView.as_view(), name='course'),
    path('course/<int:course_id>/grades/', views.course_grades, name='course_grades'),
    path('courses/add/', views.course_add, name='course_add'),
    path('courses/add2/', views.course_add2),
    path('course/<int:id>/edit/', views.CourseEditView.as_view(), name='course_edit'),

    #path('register/', views.RegisterUserView.as_view()),
    path('register/', views.register, name='registration'),
    #path('login/', views.LoginUserView.as_view()),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('receive-grade-data/', views.receive_grade_data, name='receive_grade_data'),

    ] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )