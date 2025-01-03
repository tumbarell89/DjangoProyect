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
from .models import Evaluacion, EvaluacionDetalle, Empleado
from datetime import datetime
from operator import itemgetter
from django.db.models import Avg
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font

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
    departamentos = Departamento.objects.all()
    roles = RolEmpleado.objects.all()    
    return render(request, 'empleados/gestionar_trabajadores.html', {'usuarios': usuarios, 'departamentos': departamentos, 'roles': roles})

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
        'generico': criterio.generico,
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
                    
                    if puntuacion:
                        EvaluacionDetalle.objects.update_or_create(
                            evaluacion=evaluacion,
                            empleado=empleado,
                            criterio=criterio,
                            defaults={
                                'puntuacion': puntuacion,
                            }
                        )
            
            return redirect('gestionar_evaluaciones')
    
    # Obtener evaluaciones existentes
    evaluaciones = {}
    for detalle in evaluacion.detalles.all():
        key = f"{detalle.empleado.id}_{detalle.criterio.id}"
        evaluaciones[key] = {
            'puntuacion': detalle.puntuacion,
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

@login_required
def calculo_puntuaciones(request):
    if request.method == 'POST':
        fecha_inicial = request.POST.get('fecha_inicial')
        fecha_final = request.POST.get('fecha_final')
        
        if not fecha_inicial or not fecha_final:
            return JsonResponse({'error': 'Fechas no proporcionadas'}, status=400)

        fecha_inicial = datetime.strptime(fecha_inicial, '%Y-%m-%d').date()
        fecha_final = datetime.strptime(fecha_final, '%Y-%m-%d').date()

        evaluaciones = Evaluacion.objects.filter(fecha__range=(fecha_inicial, fecha_final))
        
        if 'evaluaciones' in request.POST:
            # Cálculo de puntuaciones
            evaluaciones_ids = request.POST.getlist('evaluaciones')
            evaluaciones = Evaluacion.objects.filter(id__in=evaluaciones_ids)
            resultados = EvaluacionDetalle.get_promedios_y_sumas(evaluaciones)

            empleados = Empleado.objects.all()
            datos_empleados = []

            for empleado in empleados:
                resultado = next((r for r in resultados if r['empleado'] == empleado.id), None)
                if resultado:
                    datos_empleados.append({
                        'nombre': f"{empleado.user.first_name} {empleado.user.last_name}",
                        'promedio': resultado['promedio'],
                        'suma': resultado['suma']
                    })

            # Ordenar los resultados de mayor a menor promedio
            datos_empleados_ordenados = sorted(datos_empleados, key=itemgetter('promedio'), reverse=True)

            return JsonResponse({'empleados': datos_empleados_ordenados})
        else:
            # Búsqueda de evaluaciones
            evaluaciones_data = [{
                'id': eval.id,
                'fecha': eval.fecha.strftime('%Y-%m-%d'),
                'mes_inicial': eval.mes_inicial.strftime('%Y-%m-%d'),
                'mes_final': eval.mes_final.strftime('%Y-%m-%d')
            } for eval in evaluaciones]
            return JsonResponse({'evaluaciones': evaluaciones_data})

    return render(request, 'empleados/calculo_puntuaciones.html')

@login_required
def reportes_analisis(request):
    if request.method == 'POST':
        fecha_inicial = request.POST.get('fecha_inicial')
        fecha_final = request.POST.get('fecha_final')
        
        if not fecha_inicial or not fecha_final:
            return JsonResponse({'error': 'Fechas no proporcionadas'}, status=400)

        fecha_inicial = datetime.strptime(fecha_inicial, '%Y-%m-%d').date()
        fecha_final = datetime.strptime(fecha_final, '%Y-%m-%d').date()

        evaluaciones = Evaluacion.objects.filter(fecha__range=(fecha_inicial, fecha_final))
        
        if 'evaluaciones' in request.POST:
            evaluaciones_ids = request.POST.getlist('evaluaciones')
            evaluaciones = Evaluacion.objects.filter(id__in=evaluaciones_ids)
            
            # Calcular promedios
            promedios = EvaluacionDetalle.objects.filter(evaluacion__in=evaluaciones).values(
                'puntuacion'
            ).annotate(
                promedio=Avg('puntuacion')
            ).order_by('puntuacion')

            # Preparar datos para gráficas
            labels = [f'Puntuación {p["puntuacion"]}' for p in promedios]
            data = [float(p['promedio']) for p in promedios]

            return JsonResponse({
                'labels': labels,
                'data': data
            })
        else:
            # Búsqueda de evaluaciones
            evaluaciones_data = [{
                'id': eval.id,
                'fecha': eval.fecha.strftime('%Y-%m-%d'),
                'mes_inicial': eval.mes_inicial.strftime('%Y-%m-%d'),
                'mes_final': eval.mes_final.strftime('%Y-%m-%d')
            } for eval in evaluaciones]
            return JsonResponse({'evaluaciones': evaluaciones_data})

    return render(request, 'empleados/reportes_analisis.html')

def export_to_excel(data, filename):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Resultados"

    # Escribir encabezados
    headers = list(data[0].keys())
    for col_num, header in enumerate(headers, 1):
        col_letter = get_column_letter(col_num)
        ws[f'{col_letter}1'] = header
        ws[f'{col_letter}1'].font = Font(bold=True)

    # Escribir datos
    for row_num, row_data in enumerate(data, 2):
        for col_num, (key, value) in enumerate(row_data.items(), 1):
            ws.cell(row=row_num, column=col_num, value=value)

    # Ajustar ancho de columnas
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[get_column_letter(column_cells[0].column)].width = length + 2

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    wb.save(response)
    return response

@login_required
def reportes_analisis(request):
    if request.method == 'POST':
        fecha_inicial = request.POST.get('fecha_inicial')
        fecha_final = request.POST.get('fecha_final')
        
        if not fecha_inicial or not fecha_final:
            return JsonResponse({'error': 'Fechas no proporcionadas'}, status=400)

        fecha_inicial = datetime.strptime(fecha_inicial, '%Y-%m-%d').date()
        fecha_final = datetime.strptime(fecha_final, '%Y-%m-%d').date()

        evaluaciones = Evaluacion.objects.filter(fecha__range=(fecha_inicial, fecha_final))
        
        if 'evaluaciones' in request.POST:
            evaluaciones_ids = request.POST.getlist('evaluaciones')
            evaluaciones = Evaluacion.objects.filter(id__in=evaluaciones_ids)
            
            # Calcular promedios
            promedios = EvaluacionDetalle.objects.filter(evaluacion__in=evaluaciones).values(
                'puntuacion'
            ).annotate(
                promedio=Avg('puntuacion')
            ).order_by('puntuacion')

            # Preparar datos para gráficas y exportación
            data = [{'Puntuación': p['puntuacion'], 'Promedio': round(float(p['promedio']), 2)} for p in promedios]
            
            if 'export' in request.POST:
                return export_to_excel(data, 'reportes_analisis.xlsx')
            
            labels = [f'Puntuación {p["Puntuación"]}' for p in data]
            values = [p['Promedio'] for p in data]

            return JsonResponse({
                'labels': labels,
                'data': values
            })
        else:
            # Búsqueda de evaluaciones
            evaluaciones_data = [{
                'id': eval.id,
                'fecha': eval.fecha.strftime('%Y-%m-%d'),
                'mes_inicial': eval.mes_inicial.strftime('%Y-%m-%d'),
                'mes_final': eval.mes_final.strftime('%Y-%m-%d')
            } for eval in evaluaciones]
            return JsonResponse({'evaluaciones': evaluaciones_data})

    return render(request, 'empleados/reportes_analisis.html')
