from django.urls import path, include
from rest_framework import routers
from .views_rest import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register('persons', PersonViewSet)

urlpatterns = [
    path('v1/persons/', PersonAPIView.as_view()),
    path('v1/persons/<int:pk>/', PersonAPIView.as_view()),
    path('v1/persons/me/', CurrentUserView.as_view(), name='person-me'),

    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('v1/login/', LoginAPIView.as_view()),
    path('v1/courses/', CourseListView.as_view(), name='course_list'),
    path('v1/courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('v1/courses/<int:course_id>/users/<int:user_id>/grades/', UserGradesView.as_view(), name='graides'),
    path('v1/grades/add/', AddGradeView.as_view(), name='add-grade2'),

    path('v2/persons/', PersonAPIView2.as_view()),
    path('v2/persons/<int:pk>/edit/', PersonAPIUpdate.as_view()),
    path('v2/persons/<int:pk>/', PersonAPIDetailView.as_view()),

    path('v3/persons/', PersonViewSet.as_view({'get': "list", 'post': 'create'})),
    path('v3/persons/<int:pk>/', PersonViewSet.as_view({'get': "retrieve"})),
    path('v3/auth/', include('rest_framework.urls')),
    #path('v3/persons/int:pk/edit/', PersonViewSet.as_view({'get': ""})),

    path('v4/', include(router.urls)),

]