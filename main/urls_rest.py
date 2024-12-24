from django.urls import path, include
from rest_framework import routers
from .views_rest import *

router = routers.DefaultRouter()
router.register('persons', PersonViewSet)

urlpatterns = [
    path('v1/persons/', PersonAPIView.as_view()),
    path('v1/persons/int:pk/', PersonAPIView.as_view()),

    path('v2/persons/', PersonAPIView2.as_view()),
    path('v2/persons/int:pk/edit/', PersonAPIUpdate.as_view()),
    path('v2/persons/int:pk/', PersonAPIDetailView.as_view()),

    path('v3/persons/', PersonViewSet.as_view({'get': "list", 'post': 'create'})),
    path('v3/persons/int:pk/', PersonViewSet.as_view({'get': "retrieve"})),

    #path('v4/', include(router)),

]