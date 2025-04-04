from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Person, Course, Grade


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class PersonSerializer(serializers.ModelSerializer):
    username = UserSerializer(required=True)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=True, required=False)

    class Meta:
        model = Person
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('username')
        course_data = validated_data.pop('course', [])  # Получить список ID курсов

        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        person = Person.objects.create(username=user, **validated_data)

        person.course.set(course_data)  # Установить связь ManyToMany

        return person

class PersonSerializerKivy(serializers.ModelSerializer):
    username = serializers.CharField(source='username.username', read_only=True)

    class Meta:
        model = Person
        fields = ['id', 'username', 'name', 'surname', 'age']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class PersonSerializer2(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    age = serializers.IntegerField(max_value=100)


class UserSerializer1(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']



class PersonSerializer1(serializers.ModelSerializer):
    username = UserSerializer1(read_only=True)
    course = serializers.PrimaryKeyRelatedField(many=True, queryset=Course.objects.all())

    class Meta:
        model = Person
        fields = '__all__'
        read_only_fields = ['time_create', 'time_update']



class GradeSerializer(serializers.ModelSerializer):
    person = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), required=False, allow_null=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Grade
        fields = ['id', 'grade', 'course', 'person', 'time_create']