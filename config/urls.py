from django.contrib import admin
from django.urls import path, include
from empleados import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.perfil_empleado, name='perfil_empleado'),
    path('registrar-logro/', views.registrar_logro, name='registrar_logro'),
    path('evaluar-empleado/<int:empleado_id>/', views.evaluar_empleado, name='evaluar_empleado'),
    path('accounts/', include('django.contrib.auth.urls')),
]