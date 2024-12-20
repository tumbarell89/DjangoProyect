from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db import transaction
from .models import (
    Empleado, Departamento, RolEmpleado, CriterioEvaluacion,
    Evaluacion, EvaluacionDetalle
)
from .forms import (
    UserEmpleadoForm, CriterioEvaluacionForm, EvaluacionForm,
    EvaluacionDetalleForm
)
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    EmpleadoSerializer, DepartamentoSerializer, RolEmpleadoSerializer,
    CriterioEvaluacionSerializer, EvaluacionSerializer
)

# Existing view functions...

# ViewSets
class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
    permission_classes = [IsAuthenticated]

class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAuthenticated]

class RolEmpleadoViewSet(viewsets.ModelViewSet):
    queryset = RolEmpleado.objects.all()
    serializer_class = RolEmpleadoSerializer
    permission_classes = [IsAuthenticated]

class CriterioEvaluacionViewSet(viewsets.ModelViewSet):
    queryset = CriterioEvaluacion.objects.all()
    serializer_class = CriterioEvaluacionSerializer
    permission_classes = [IsAuthenticated]

class EvaluacionViewSet(viewsets.ModelViewSet):
    queryset = Evaluacion.objects.all()
    serializer_class = EvaluacionSerializer
    permission_classes = [IsAuthenticated]

# Keep all existing view functions...

@login_required
def gestionar_trabajadores(request):
    usuarios = User.objects.filter(activo=True)
    return render(request, 'empleados/gestionar_trabajadores.html', {'usuarios': usuarios})

@login_required
@require_http_methods(["POST"])
def crear_editar_trabajador(request):
    user_id = request.POST.get('user_id')
    if user_id:
        user = get_object_or_404(User, id=user_id)
        form = UserEmpleadoForm(request.POST, instance=user)
    else:
        form = UserEmpleadoForm(request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
@require_http_methods(["POST"])
def eliminar_trabajador(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.activo = False
    user.save()
    return JsonResponse({'status': 'success'})

@login_required
@require_http_methods(["GET"])
def obtener_trabajador(request, user_id):
    user = get_object_or_404(User, id=user_id)
    empleado = user.empleado if hasattr(user, 'empleado') else None
    data = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'is_superuser': user.is_superuser,
        'activo': user.activo,
        'departamento': empleado.departamento.id if empleado and empleado.departamento else None,
        'rol': empleado.rol.id if empleado and empleado.rol else None,
        'habilidades': empleado.habilidades if empleado else '',
        'aptitudes': empleado.aptitudes if empleado else '',
        'competencias': empleado.competencias if empleado else '',
    }
    return JsonResponse(data)

@login_required
def gestionar_criterios_evaluacion(request):
    criterios = CriterioEvaluacion.objects.all()
    roles = RolEmpleado.objects.all()
    return render(request, 'empleados/gestionar_criterios_evaluacion.html', {'criterios': criterios, 'roles': roles})

@login_required
@require_http_methods(["POST"])
def crear_editar_criterio(request):
    criterio_id = request.POST.get('criterio_id')
    if criterio_id:
        criterio = get_object_or_404(CriterioEvaluacion, id=criterio_id)
        form = CriterioEvaluacionForm(request.POST, instance=criterio)
    else:
        form = CriterioEvaluacionForm(request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
@require_http_methods(["POST"])
def eliminar_criterio(request, criterio_id):
    criterio = get_object_or_404(CriterioEvaluacion, id=criterio_id)
    criterio.delete()
    return JsonResponse({'status': 'success'})

@login_required
@require_http_methods(["GET"])
def obtener_criterio(request, criterio_id):
    criterio = get_object_or_404(CriterioEvaluacion, id=criterio_id)
    data = {
        'id': criterio.id,
        'denominacion': criterio.denominacion,
        'rol': criterio.rol.id,
    }
    return JsonResponse(data)

@login_required
def gestionar_evaluaciones(request):
    evaluaciones = Evaluacion.objects.all()
    return render(request, 'empleados/gestionar_evaluaciones.html', {
        'evaluaciones': evaluaciones
    })

@login_required
def crear_evaluacion(request):
    if request.method == 'POST':
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            evaluacion = form.save(commit=False)
            evaluacion.autor = request.user
            evaluacion.save()
            return redirect('editar_evaluacion', evaluacion_id=evaluacion.id)
    else:
        form = EvaluacionForm()
    
    return render(request, 'empleados/crear_evaluacion.html', {
        'form': form
    })

@login_required
def editar_evaluacion(request, evaluacion_id):
    evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id)
    empleados = Empleado.objects.filter(user__activo=True)
    criterios = CriterioEvaluacion.objects.all()
    
    if request.method == 'POST':
        with transaction.atomic():
            for empleado in empleados:
                for criterio in criterios:
                    puntuacion = request.POST.get(f'puntuacion_{empleado.id}_{criterio.id}')
                    concepto = request.POST.get(f'concepto_{empleado.id}_{criterio.id}', '')
                    
                    if puntuacion:
                        EvaluacionDetalle.objects.update_or_create(
                            evaluacion=evaluacion,
                            empleado=empleado,
                            criterio=criterio,
                            defaults={
                                'puntuacion': puntuacion,
                                'concepto': concepto
                            }
                        )
            
            return redirect('gestionar_evaluaciones')
    
    # Obtener evaluaciones existentes
    evaluaciones = {}
    for detalle in evaluacion.detalles.all():
        key = f"{detalle.empleado.id}_{detalle.criterio.id}"
        evaluaciones[key] = {
            'puntuacion': detalle.puntuacion,
            'concepto': detalle.concepto
        }
    
    return render(request, 'empleados/editar_evaluacion.html', {
        'evaluacion': evaluacion,
        'empleados': empleados,
        'criterios': criterios,
        'evaluaciones': evaluaciones
    })

@login_required
def eliminar_evaluacion(request, evaluacion_id):
    evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id)
    if request.method == 'POST':
        evaluacion.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

