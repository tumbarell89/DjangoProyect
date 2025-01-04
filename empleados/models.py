from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Sum

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
    generico = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.denominacion} - {self.rol}"

class Evaluacion(models.Model):
    fecha = models.DateField(auto_now_add=True)
    mes_inicial = models.DateField()
    mes_final = models.DateField()
    autor = models.ForeignKey(User, on_delete=models.PROTECT)
    
    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"Evaluación del {self.mes_inicial} al {self.mes_final}"
    
    @classmethod
    def get_evaluaciones_en_rango(cls, fecha_inicial, fecha_final):
        return cls.objects.filter(fecha__range=(fecha_inicial, fecha_final))

class EvaluacionDetalle(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name='detalles')
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT)
    criterio = models.ForeignKey(CriterioEvaluacion, on_delete=models.PROTECT)
    puntuacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        unique_together = ['evaluacion', 'empleado', 'criterio']

    def __str__(self):
        return f"Evaluación de {self.empleado} - {self.criterio}"

    @classmethod
    def get_promedios_y_sumas(cls, evaluaciones, excluir_genericos=True):
        detalles = cls.objects.filter(evaluacion__in=evaluaciones)
        if excluir_genericos:
            detalles2 = detalles.exclude(criterio__generico=True)
        
        return detalles.values('empleado').annotate(
            promedio=Avg('puntuacion'),
            suma=Avg(detalles2.values())
        )
    
# Añadir un campo 'activo' al modelo User
User.add_to_class('activo', models.BooleanField(default=True))

