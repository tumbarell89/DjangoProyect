from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import Empleado, Logro, Evaluacion, Ranking
from .forms import LogroForm, EvaluacionForm, EmpleadoForm

@login_required
def perfil_empleado(request):
    try:
        empleado = request.user.empleado
    except ObjectDoesNotExist:
        return redirect('crear_empleado')
    
    logros = Logro.objects.filter(empleado=empleado)
    evaluaciones = Evaluacion.objects.filter(empleado=empleado)
    ranking = Ranking.objects.filter(empleado=empleado).order_by('-fecha').first()
    
    context = {
        'empleado': empleado,
        'logros': logros,
        'evaluaciones': evaluaciones,
        'ranking': ranking,
    }
    return render(request, 'empleados/perfil.html', context)

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