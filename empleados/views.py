from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Empleado
from .forms import EmpleadoForm
from .serializers import EmpleadoSerializer, UserSerializer

@login_required
def crear_empleado(request):
    if hasattr(request.user, 'empleado'):
        return redirect('perfil_empleado')
    
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            empleado = form.save(commit=False)
            empleado.user = request.user
            empleado.save()
            return redirect('perfil_empleado')
    else:
        form = EmpleadoForm()
    
    return render(request, 'empleados/crear_empleado.html', {'form': form})

@login_required
def gestion_evaluaciones(request):
    # Implementar lógica para gestión de evaluaciones
    return render(request, 'empleados/gestion_evaluaciones.html')

@login_required
def registro_logros(request):
    if request.method == 'POST':
        form = LogroForm(request.POST, request.FILES)
        if form.is_valid():
            logro = form.save(commit=False)
            logro.empleado = request.user.empleado
            logro.save()
            return redirect('perfil_empleado')
    else:
        form = LogroForm()
    return render(request, 'empleados/registro_logros.html', {'form': form})

@login_required
def calculo_puntuaciones(request):
    # Implementar lógica para cálculo de puntuaciones
    return render(request, 'empleados/calculo_puntuaciones.html')

@login_required
def reportes_analisis(request):
    # Implementar lógica para reportes y análisis
    return render(request, 'empleados/reportes_analisis.html')


@login_required
def dashboard(request):
    return render(request, 'empleados/dashboard.html')

@login_required
def lista_perfiles(request):
    perfiles = Empleado.objects.all()
    return render(request, 'empleados/lista_perfiles.html', {'perfiles': perfiles})

@login_required
def crear_perfil(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_perfiles')
    else:
        form = EmpleadoForm()
    return render(request, 'empleados/crear_editar_perfil.html', {'form': form})

@login_required
def editar_perfil(request, pk):
    perfil = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('lista_perfiles')
    else:
        form = EmpleadoForm(instance=perfil)
    return render(request, 'empleados/crear_editar_perfil.html', {'form': form})

@login_required
def eliminar_perfil(request, pk):
    perfil = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        perfil.delete()
        return redirect('lista_perfiles')
    return render(request, 'empleados/confirmar_eliminar_perfil.html', {'perfil': perfil})

@login_required
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'empleados/lista_usuarios.html', {'usuarios': usuarios})

# API Views
class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['GET'])
@login_required
def api_dashboard(request):
    # Implement dashboard logic here
    return Response({"message": "Dashboard data"})

@api_view(['GET'])
@login_required
def api_lista_perfiles(request):
    perfiles = Empleado.objects.all()
    serializer = EmpleadoSerializer(perfiles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@login_required
def api_lista_usuarios(request):
    usuarios = User.objects.all()
    serializer = UserSerializer(usuarios, many=True)
    return Response(serializer.data)

