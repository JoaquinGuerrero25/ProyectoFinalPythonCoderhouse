from django import forms
from .models import Publicacion, EdicionPublicacion, Comentario

class PublicacionForm(forms.ModelForm):
    imagen = forms.ImageField(required=True)
    class Meta:
        model = Publicacion
        fields = ['titulo', 'contenido', 'imagen']

class EdicionPublicacionForm(forms.ModelForm):
    class Meta:
        model = EdicionPublicacion
        fields = ['contenido_nuevo']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']