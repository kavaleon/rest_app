from rest_framework import serializers
from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        #fields = ['surname', "name"]
        fields = '__all__'


class PerdonSerializer2(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    age = serializers.IntegerField(max_value=100)