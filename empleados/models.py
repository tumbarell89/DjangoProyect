from django.db import models
from django.contrib.auth.models import User

class Departamento(models.Model):
    denominacion = models.CharField(max_length=100)

    def __str__(self):
        return self.denominacion

class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empleado')
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True)
    habilidades = models.TextField(blank=True)
    aptitudes = models.TextField(blank=True)
    competencias = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

# Añadir un campo 'activo' al modelo User
User.add_to_class('activo', models.BooleanField(default=True))



class CriterioEvaluacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    peso = models.FloatField()
    rol = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Logro(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha = models.DateField()
    evidencia = models.FileField(upload_to='evidencias/', null=True, blank=True)

    def __str__(self):
        return f"{self.empleado.user.username} - {self.fecha}"

class Evaluacion(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    criterio = models.ForeignKey(CriterioEvaluacion, on_delete=models.CASCADE)
    puntuacion = models.FloatField()
    fecha = models.DateField()

    def __str__(self):
        return f"{self.empleado.user.username} - {self.criterio.nombre}"

class Ranking(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    puntuacion_total = models.FloatField()
    posicion_departamento = models.IntegerField()
    posicion_global = models.IntegerField()
    fecha = models.DateField()

    def __str__(self):
        return f"{self.empleado.user.username} - Posición: {self.posicion_global}"