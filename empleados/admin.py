from django.contrib import admin
from .models import (
    Habilidad, 
    Aptitud, 
    Competencia, 
    Departamento, 
    RolEmpleado
)

# Registrar los modelos de nomencladores
@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Aptitud)
class AptitudAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Competencia)
class CompetenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

# Registrar otros modelos
@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('denominacion',)
    search_fields = ('denominacion',)

@admin.register(RolEmpleado)
class RolEmpleadoAdmin(admin.ModelAdmin):
    list_display = ('denominacion',)
    search_fields = ('denominacion',)

