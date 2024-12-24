from rest_framework.response import Response
from .models import Person
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from rest_framework import generics
from .serializers import PersonSerializer
from rest_framework import viewsets

#version 1
class PersonAPIView(APIView):
    def get(self, r, **kwargs):
        if kwargs.get('pk', None):
            pass #берем одну запись
        persons = Person.objects.all().values()
        return Response({'data': list(persons)})
    # filter ---- Person.object.filter(name="filter")
    # filter ---- Person.object.filter(name__contains='filter')

    # def put(self, id, **kwargs):
    #     person = Person.object.get(id=id)
    #     if name:
    #         person.name = name
    #     person.save()
    #     return Response({"person": model_to_dict(person)})

    def delete(self, id):
        persons = Person.objects.get(id=5).delete()
        return Response({'data': list(persons)})

    def post(self, r):
        name = r.data['name']
        surname = r.data['surname']
        age = r.data['age']
        age2 = r.data['age2']
        person = Person(name=name, surname=surname, age=age, age2=age2)
        person.save()
        #person = Person.objects.create(name=name, surname=surname, age=age, age2=age2)
        return Response({"person": model_to_dict(person)})

#version 2
class PersonAPIView2(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class PersonAPIUpdate(generics.UpdateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class PersonAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


#version 3

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer



