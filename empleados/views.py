from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Empleado, Logro, Evaluacion, Ranking
from .forms import LogroForm, EvaluacionForm

@login_required
def perfil_empleado(request):
    empleado = request.user.empleado
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
def registrar_logro(request):
    if request.method == 'POST':
        form = LogroForm(request.POST, request.FILES)
        if form.is_valid():
            logro = form.save(commit=False)
            logro.empleado = request.user.empleado
            logro.save()
            return redirect('perfil_empleado')
    else:
        form = LogroForm()
    return render(request, 'empleados/registrar_logro.html', {'form': form})

@login_required
def evaluar_empleado(request, empleado_id):
    if not request.user.is_staff:
        return redirect('perfil_empleado')
    
    empleado = Empleado.objects.get(id=empleado_id)
    if request.method == 'POST':
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            evaluacion = form.save(commit=False)
            evaluacion.empleado = empleado
            evaluacion.save()
            return redirect('perfil_empleado')
    else:
        form = EvaluacionForm()
    return render(request, 'empleados/evaluar_empleado.html', {'form': form, 'empleado': empleado})