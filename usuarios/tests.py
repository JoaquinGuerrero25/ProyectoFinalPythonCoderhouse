from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import SESSION_KEY, authenticate, login
from django.contrib.messages import get_messages
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from usuarios.views import (IniciarSesion, editar_usuario, cambiar_contrasena,
                            agregar_avatar, ver_mi_perfil, ver_perfil,
                            cerrar_sesion, acerca_de_mi)
from usuarios.forms import EditarUsuarioForm, AgregarAvatarForm
from publicaciones.models import Publicacion
from usuarios.models import Avatar
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import logout


class RequestMock(Client):
    def request(self, **request):
        request = super().request(**request)
        request.session = SessionStore()
        return request

class UsuariosTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='prueba',
            password='contrasena1',
            email='email@gmail.com',
            first_name='name',
            last_name='name12'
        )
        self.avatar = Avatar.objects.create(user=self.user)
        self.publicacion = Publicacion.objects.create(creador=self.user)

    def test_iniciar_sesion(self):
        form_data = {
            'username': 'prueba',
            'password': 'contrasena1'
        }
        response = self.client.post(reverse('perfil:login'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pages:lista_publicaciones'))

    def test_editar_usuario(self):
        self.client.force_login(self.user)
        form_data = {
            'username': 'prueba_editado',
            'first_name': 'name_editado',
            'last_name': 'name12_editado',
            'email': 'email_editado@gmail.com'
        }
        response = self.client.post(reverse('usuarios:editar_usuario'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('perfil:mi_perfil'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'prueba_editado')
        self.assertEqual(self.user.first_name, 'name_editado')
        self.assertEqual(self.user.last_name, 'name12_editado')
        self.assertEqual(self.user.email, 'email_editado@gmail.com')

    def test_cambiar_contrasena(self):
        self.client.force_login(self.user)
        form_data = {
            'old_password': 'contrasena1',
            'new_password1': 'nueva_contrasena',
            'new_password2': 'nueva_contrasena'
        }
        response = self.client.post(reverse('perfil:cambiar_contrasena'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('perfil:mi_perfil'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('nueva_contrasena'))

    def test_ver_mi_perfil(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('perfil:mi_perfil'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/perfil.html')

    def test_ver_perfil(self):
        response = self.client.get(reverse('perfil:ver_perfil', args=['prueba']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/perfil_autor.html')

class CerrarSesionTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='prueba',
            password='contrasena1',
            email='email@gmail.com',
            first_name='name',
            last_name='name12'
        )
        self.avatar = Avatar.objects.create(user=self.user)
        self.publicacion = Publicacion.objects.create(creador=self.user)

    def test_cerrar_sesion(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('perfil:cerrar_sesion'))
        session = self.client.session
        self.assertNotIn('_auth_user_id', session)
        self.assertRedirects(response, reverse('pages:lista_publicaciones'))

class AgregarAvatarTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='prueba',
            password='contrasena1',
            email='email@gmail.com',
            first_name='name',
            last_name='name12'
        )

    def test_agregar_avatar(self):
        self.client.force_login(self.user)
        image = SimpleUploadedFile("fotodeperfil.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.post(reverse('perfil:agregar_avatar'), {'avatar': image})
        self.assertEqual(response.status_code, 302)
        avatar = Avatar.objects.get(user=self.user)
        self.assertIsNotNone(avatar)
        self.assertEqual(avatar.photo.name, 'usuarios/img/fotodeperfil.jpg')
        self.assertRedirects(response, reverse('perfil:mi_perfil'))
