from django.db import models
from django.contrib.auth.models import User

class Publicacion(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='publicaciones/')
    creador = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class EdicionPublicacion(models.Model):
    publicacion = models.OneToOneField(Publicacion, on_delete=models.CASCADE)
    editor = models.ForeignKey(User, on_delete=models.CASCADE)

    fecha_edicion = models.DateTimeField(auto_now=True)
    contenido_nuevo = models.TextField()

    def __str__(self):
        return f"Edición de '{self.publicacion.titulo}' por {self.editor.username}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.editor = self.publicacion.creador
        return super().save(*args, **kwargs)

class Comentario(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de '{self.autor.username}' en '{self.publicacion.titulo}'"