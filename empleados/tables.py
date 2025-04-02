import django_tables2 as tables
from django.contrib.auth.models import User
from .models import Empleado, CriterioEvaluacion, Evaluacion
from django.utils.html import format_html

class UserEmpleadoTable(tables.Table):
    nombre = tables.Column(accessor='first_name', verbose_name='Nombre')
    apellido = tables.Column(accessor='last_name', verbose_name='Apellido')
    email = tables.Column(accessor='email', verbose_name='Email')
    departamento = tables.Column(accessor='empleado.departamento.denominacion', verbose_name='Departamento', empty_values=())
    rol = tables.Column(accessor='empleado.rol.denominacion', verbose_name='Rol', empty_values=())
    acciones = tables.TemplateColumn(
        template_name='empleados/tables/user_actions.html',
        verbose_name='Acciones',
        orderable=False,
        exclude_from_export=True
    )

    def render_departamento(self, value, record):
        try:
            return record.empleado.departamento.denominacion if record.empleado.departamento else ""
        except:
            return ""

    def render_rol(self, value, record):
        try:
            return record.empleado.rol.denominacion if record.empleado.rol else ""
        except:
            return ""

    class Meta:
        model = User
        template_name = "django_tables2/bootstrap4.html"
        fields = ('nombre', 'apellido', 'email', 'departamento', 'rol', 'acciones')
        attrs = {"class": "min-w-full leading-normal"}
        row_attrs = {
            "class": "border-b border-gray-200 hover:bg-gray-100"
        }
        order_by = 'nombre'

class CriterioEvaluacionTable(tables.Table):
    denominacion = tables.Column(verbose_name='Denominación')
    rol = tables.Column(accessor='rol.denominacion', verbose_name='Rol', empty_values=())
    generico = tables.BooleanColumn(verbose_name='Genérico')
    acciones = tables.TemplateColumn(
        template_name='empleados/tables/criterio_actions.html',
        verbose_name='Acciones',
        orderable=False,
        exclude_from_export=True
    )

    def render_rol(self, value, record):
        return record.rol.denominacion if record.rol else ""

    class Meta:
        model = CriterioEvaluacion
        template_name = "django_tables2/bootstrap4.html"
        fields = ('denominacion', 'rol', 'generico', 'acciones')
        attrs = {"class": "min-w-full leading-normal"}
        row_attrs = {
            "class": "border-b border-gray-200 hover:bg-gray-100"
        }
        order_by = 'denominacion'

class EvaluacionTable(tables.Table):
    fecha = tables.DateColumn(format='d/m/Y', verbose_name='Fecha')
    periodo = tables.Column(empty_values=(), verbose_name='Período')
    autor = tables.Column(empty_values=(), verbose_name='Autor')
    acciones = tables.TemplateColumn(
        template_name='empleados/tables/evaluacion_actions.html',
        verbose_name='Acciones',
        orderable=False,
        exclude_from_export=True
    )

    def render_periodo(self, record):
        return f"{record.mes_inicial.strftime('%m/%Y')} - {record.mes_final.strftime('%m/%Y')}"
    
    def render_autor(self, record):
        return f"{record.autor}"
        

    class Meta:
        model = Evaluacion
        template_name = "django_tables2/bootstrap4.html"
        fields = ('fecha', 'periodo', 'autor', 'acciones')
        attrs = {"class": "min-w-full leading-normal"}
        row_attrs = {
            "class": "border-b border-gray-200 hover:bg-gray-100"
        }
        order_by = '-fecha'

