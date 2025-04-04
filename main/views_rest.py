from django.contrib.auth import authenticate
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Person, Course, Grade
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from rest_framework import generics, status
from .serializers import PersonSerializer, PersonSerializer2, UserSerializer1, CourseSerializer, PersonSerializer1, \
    PersonSerializerKivy, GradeSerializer
from rest_framework import viewsets
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication


#version 1

class PersonAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if pk:
            try:
                person = Person.objects.get(pk=pk)
                serializer = PersonSerializer(person)
                return Response({"data": serializer.data})
            except Person.DoesNotExist:
                raise Http404("Пользователь не найден")

        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk):
        """
        Обновление существующего пользователя.
        """
        try:
            person = Person.objects.get(pk=pk)
        except Person.DoesNotExist:
            raise Http404("Пользователь не найден")

        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"person": serializer.data})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Удаление пользователя.
        """
        try:
            person = Person.objects.get(pk=pk)
        except Person.DoesNotExist:
            raise Http404("Пользователь не найден")

        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        person = request.user.person
        serializer = PersonSerializerKivy(person)
        return Response({"data": serializer.data})


#version 2
class PersonAPIView2(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer2
    permission_classes = (IsAuthenticated, IsAuthenticatedOrReadOnly)

class PersonAPIUpdate(generics.UpdateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer2
    permission_classes = (IsAdminOrReadOnly,)

class PersonAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer2


#version 3
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer2

class GradeCreateView(generics.CreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


class LoginAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer1

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({"message": "Login successful", "user": UserSerializer1(user).data})
        return Response({"error": "Invalid username or password"}, status=400)

class CourseListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication] # вход только по токену

    def get(self, request):
        user = request.user
        person = Person.objects.get(username=user)
        courses = person.course.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class UserGradesView(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request, course_id, user_id):
        grades = Grade.objects.filter(course=course_id, person=user_id)
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)

class AddGradeView(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, request, course_id, user_id):
        print(course_id, user_id)
        data = request.data
        print(data)
        data['grade'] = int(data['grade'])
        data['course'] = course_id
        data['person'] = user_id
        print(data)
        serializer = GradeSerializer(data=data)
        if serializer.is_valid():
            print('ok')
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class AddGradeView(generics.CreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        course_id = data.get('course_id')
        person_id = data.get('person_id')

        # Получение объектов Course и Person по их идентификаторам
        course = get_object_or_404(Course, id=course_id)
        person = get_object_or_404(Person, id=person_id)

        # Создание сериализатора с данными
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)