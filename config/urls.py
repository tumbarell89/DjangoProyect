from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from empleados import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('gestionar-trabajadores/', views.gestionar_trabajadores, name='gestionar_trabajadores'),
    path('crear-editar-trabajador/', views.crear_editar_trabajador, name='crear_editar_trabajador'),
    path('eliminar-trabajador/<int:user_id>/', views.eliminar_trabajador, name='eliminar_trabajador'),
    path('obtener-trabajador/<int:user_id>/', views.obtener_trabajador, name='obtener_trabajador'),
    path('gestionar-criterios-evaluacion/', views.gestionar_criterios_evaluacion, name='gestionar_criterios_evaluacion'),
    path('crear-editar-criterio/', views.crear_editar_criterio, name='crear_editar_criterio'),
    path('eliminar-criterio/<int:criterio_id>/', views.eliminar_criterio, name='eliminar_criterio'),
    path('obtener-criterio/<int:criterio_id>/', views.obtener_criterio, name='obtener_criterio'),
    
    # API URLs
    path('api/', include(router.urls)),

]

