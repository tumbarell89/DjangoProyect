from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Empleado, Departamento, RolEmpleado, CriterioEvaluacion, Evaluacion, EvaluacionDetalle

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_superuser', 'activo']

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ['id', 'denominacion']

class RolEmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolEmpleado
        fields = ['id', 'denominacion']

class EmpleadoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    departamento = DepartamentoSerializer()
    rol = RolEmpleadoSerializer()

    class Meta:
        model = Empleado
        fields = ['id', 'user', 'departamento', 'rol', 'habilidades', 'aptitudes', 'competencias']

class CriterioEvaluacionSerializer(serializers.ModelSerializer):
    rol = RolEmpleadoSerializer()

    class Meta:
        model = CriterioEvaluacion
        fields = ['id', 'denominacion', 'rol']

class EvaluacionDetalleSerializer(serializers.ModelSerializer):
    empleado = EmpleadoSerializer()
    criterio = CriterioEvaluacionSerializer()

    class Meta:
        model = EvaluacionDetalle
        fields = ['id', 'evaluacion', 'empleado', 'criterio', 'puntuacion', 'concepto']

class EvaluacionSerializer(serializers.ModelSerializer):
    autor = UserSerializer()
    detalles = EvaluacionDetalleSerializer(many=True, read_only=True)

    class Meta:
        model = Evaluacion
        fields = ['id', 'fecha', 'mes_inicial', 'mes_final', 'autor', 'detalles']

