from django import forms
from django.contrib.auth.models import User
from .models import Empleado, Departamento, RolEmpleado, CriterioEvaluacion, Evaluacion, EvaluacionDetalle, Habilidad, Aptitud, Competencia

class UserEmpleadoForm(forms.ModelForm):
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all(), required=False)
    rol = forms.ModelChoiceField(queryset=RolEmpleado.objects.all(), required=False)
    habilidades = forms.ModelMultipleChoiceField(
        queryset=Habilidad.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'select2-multiple',
            'style': 'width: 100%',
            'multiple': 'multiple'
        }),
        required=False
    )
    aptitudes = forms.ModelMultipleChoiceField(
        queryset=Aptitud.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'select2-multiple',
            'style': 'width: 100%',
            'multiple': 'multiple'
        }),
        required=False
    )
    competencias = forms.ModelMultipleChoiceField(
        queryset=Competencia.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'select2-multiple',
            'style': 'width: 100%',
            'multiple': 'multiple'
        }),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'activo', 
                 'departamento', 'rol', 'habilidades', 'aptitudes', 'competencias']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            empleado, created = Empleado.objects.get_or_create(user=user)
            empleado.departamento = self.cleaned_data['departamento']
            empleado.rol = self.cleaned_data['rol']
            empleado.save()
            
            # Limpiar y establecer relaciones ManyToMany
            empleado.habilidades.clear()
            empleado.habilidades.add(*self.cleaned_data['habilidades'])
            
            empleado.aptitudes.clear()
            empleado.aptitudes.add(*self.cleaned_data['aptitudes'])
            
            empleado.competencias.clear()
            empleado.competencias.add(*self.cleaned_data['competencias'])
        return user

class CriterioEvaluacionForm(forms.ModelForm):
    class Meta:
        model = CriterioEvaluacion
        fields = ['denominacion', 'rol', 'generico']

class EvaluacionForm(forms.ModelForm):
    mes_inicial = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    mes_final = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Evaluacion
        fields = ['mes_inicial', 'mes_final']

class EvaluacionDetalleForm(forms.ModelForm):
    class Meta:
        model = EvaluacionDetalle
        fields = ['puntuacion']

