from django.db import models
from django.contrib.auth.models import User

class Departamento(models.Model):
    denominacion = models.CharField(max_length=100)

    def __str__(self):
        return self.denominacion

class RolEmpleado(models.Model):
    denominacion = models.CharField(max_length=100)

    def __str__(self):
        return self.denominacion

class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empleado')
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True)
    rol = models.ForeignKey(RolEmpleado, on_delete=models.SET_NULL, null=True)
    habilidades = models.TextField(blank=True)
    aptitudes = models.TextField(blank=True)
    competencias = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class CriterioEvaluacion(models.Model):
    denominacion = models.CharField(max_length=200)
    rol = models.ForeignKey(RolEmpleado, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.denominacion} - {self.rol}"

# Añadir un campo 'activo' al modelo User
User.add_to_class('activo', models.BooleanField(default=True))

