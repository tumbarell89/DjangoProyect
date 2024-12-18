from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Empleado, Departamento
from .forms import UserEmpleadoForm
from django.views.decorators.http import require_http_methods

@login_required
def gestionar_trabajadores(request):
    usuarios = User.objects.filter(activo=True)
    departamentos = Departamento.objects.all()
    return render(request, 'empleados/gestionar_trabajadores.html', {
        'usuarios': usuarios,
        'departamentos': departamentos
    })

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
        'habilidades': empleado.habilidades if empleado else '',
        'aptitudes': empleado.aptitudes if empleado else '',
        'competencias': empleado.competencias if empleado else '',
    }

    return JsonResponse(data)

    ##API Views
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


