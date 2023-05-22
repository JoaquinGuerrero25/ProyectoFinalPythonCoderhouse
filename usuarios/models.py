from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos', blank=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)

    def __str__(self):
        return self.usuario.username


class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    photo = models.ImageField(upload_to='avatars/', default='usuarios/img/fotodeperfil.jpg')
