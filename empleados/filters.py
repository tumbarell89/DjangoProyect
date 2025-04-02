import django_filters
from django.contrib.auth.models import User
from .models import CriterioEvaluacion, Evaluacion
from django.db import models


class UserEmpleadoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains', label='Nombre')
    departamento = django_filters.CharFilter(field_name='empleado__departamento__denominacion', lookup_expr='icontains', label='Departamento')

    class Meta:
        model = User
        fields = ['nombre', 'departamento']

class CriterioEvaluacionFilter(django_filters.FilterSet):
    denominacion = django_filters.CharFilter(lookup_expr='icontains', label='Denominación')
    rol = django_filters.CharFilter(field_name='rol__denominacion', lookup_expr='icontains', label='Rol')

    class Meta:
        model = CriterioEvaluacion
        fields = ['denominacion', 'rol']

class EvaluacionFilter(django_filters.FilterSet):
    fecha_desde = django_filters.DateFilter(field_name='fecha', lookup_expr='gte', label='Fecha desde')
    fecha_hasta = django_filters.DateFilter(field_name='fecha', lookup_expr='lte', label='Fecha hasta')
    autor = django_filters.CharFilter(method='filter_autor', label='Autor')

    class Meta:
        model = Evaluacion
        fields = ['fecha_desde', 'fecha_hasta', 'autor']
    
    def filter_autor(self, queryset, name, value):
        # Buscar por nombre, apellido o nombre de usuario
        return queryset.filter(
            models.Q(autor__first_name__icontains=value) | 
            models.Q(autor__last_name__icontains=value) | 
            models.Q(autor__username__icontains=value)
        )

