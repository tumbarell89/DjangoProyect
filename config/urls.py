from django.contrib import admin
from django.urls import path, include
from empleados import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.perfil_empleado, name='perfil_empleado'),
    path('crear-empleado/', views.crear_empleado, name='crear_empleado'),
    path('gestion-evaluaciones/', views.gestion_evaluaciones, name='gestion_evaluaciones'),
    path('registro-logros/', views.registro_logros, name='registro_logros'),
    path('calculo-puntuaciones/', views.calculo_puntuaciones, name='calculo_puntuaciones'),
    path('reportes-analisis/', views.reportes_analisis, name='reportes_analisis'),
    path('accounts/', include('django.contrib.auth.urls')),
]

