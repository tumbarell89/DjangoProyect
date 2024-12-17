from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Empleado

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class EmpleadoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Empleado
        fields = ['id', 'user', 'departamento', 'habilidades', 'aptitudes', 'competencias']

