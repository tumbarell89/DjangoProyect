from django import forms
from .models import Logro, Evaluacion

class LogroForm(forms.ModelForm):
    class Meta:
        model = Logro
        fields = ['descripcion', 'fecha', 'evidencia']

class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = ['criterio', 'puntuacion', 'fecha']