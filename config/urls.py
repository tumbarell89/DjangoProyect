from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from empleados import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'empleados', views.EmpleadoViewSet)
router.register(r'usuarios', views.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.perfil_empleado, name='perfil_empleado'),
    path('crear-empleado/', views.crear_empleado, name='crear_empleado'),
    path('gestion-evaluaciones/', views.gestion_evaluaciones, name='gestion_evaluaciones'),
    path('registro-logros/', views.registro_logros, name='registro_logros'),
    path('calculo-puntuaciones/', views.calculo_puntuaciones, name='calculo_puntuaciones'),
    path('reportes-analisis/', views.reportes_analisis, name='reportes_analisis'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfiles/', views.lista_perfiles, name='lista_perfiles'),
    path('perfiles/crear/', views.crear_perfil, name='crear_perfil'),
    path('perfiles/editar/<int:pk>/', views.editar_perfil, name='editar_perfil'),
    path('perfiles/eliminar/<int:pk>/', views.eliminar_perfil, name='eliminar_perfil'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    
    # API URLs
    path('api/', include(router.urls)),
    path('api/dashboard/', views.api_dashboard, name='api_dashboard'),
    path('api/perfiles/', views.api_lista_perfiles, name='api_lista_perfiles'),
    path('api/usuarios/', views.api_lista_usuarios, name='api_lista_usuarios'),

]

