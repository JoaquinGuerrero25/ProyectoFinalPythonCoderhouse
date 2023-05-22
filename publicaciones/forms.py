from django import forms
from .models import Publicacion, EdicionPublicacion, Comentario

class PublicacionForm(forms.ModelForm):
    imagen = forms.ImageField(required=True)
    class Meta:
        model = Publicacion
        fields = ['titulo', 'contenido', 'imagen']

class Formulario_Editar(forms.ModelForm):
    class Meta:
        model = EdicionPublicacion
        fields = ('contenido',)
        labels = {'contenido': 'Contenido'}

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']