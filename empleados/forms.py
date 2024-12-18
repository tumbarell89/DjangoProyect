from django import forms
from django.contrib.auth.models import User
from .models import Empleado, Departamento, RolEmpleado, CriterioEvaluacion

class UserEmpleadoForm(forms.ModelForm):
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all(), required=False)
    rol = forms.ModelChoiceField(queryset=RolEmpleado.objects.all(), required=False)
    habilidades = forms.CharField(widget=forms.Textarea, required=False)
    aptitudes = forms.CharField(widget=forms.Textarea, required=False)
    competencias = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_superuser', 'activo', 
                  'departamento', 'rol', 'habilidades', 'aptitudes', 'competencias']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            empleado, created = Empleado.objects.get_or_create(user=user)
            empleado.departamento = self.cleaned_data['departamento']
            empleado.rol = self.cleaned_data['rol']
            empleado.habilidades = self.cleaned_data['habilidades']
            empleado.aptitudes = self.cleaned_data['aptitudes']
            empleado.competencias = self.cleaned_data['competencias']
            empleado.save()
        return user

class CriterioEvaluacionForm(forms.ModelForm):
    class Meta:
        model = CriterioEvaluacion
        fields = ['denominacion', 'rol']

