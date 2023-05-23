from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from publicaciones.models import Publicacion, EdicionPublicacion, Comentario
from publicaciones.forms import PublicacionForm, ComentarioForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages


class PublicacionesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='prueba',
            password='contrasena1',
            email='email@gmail.com',
            first_name='name',
            last_name='name12'
        )

    def test_listar_publicaciones(self):
        Publicacion.objects.create(
            titulo='Título de prueba',
            contenido='Contenido de prueba',
            imagen='publicaciones/test_image.jpg',
            creador=self.user
        )
        response = self.client.get(reverse('pages:lista_publicaciones'))
        self.assertEqual(response.status_code, 200)
        publicaciones = response.context['publicaciones']
        self.assertEqual(publicaciones.count(), 1)
        self.assertEqual(publicaciones[0].titulo, 'Título de prueba')

    def test_detalle_publicacion(self):
        # Crear una publicación de prueba
        publicacion = Publicacion.objects.create(
            titulo='Título de prueba',
            contenido='Contenido de prueba',
            imagen='publicaciones/test_image.jpg',
            creador=self.user
        )
        response = self.client.get(reverse('pages:detalle_publicacion', args=[publicacion.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['publicacion'].titulo, 'Título de prueba')

    def test_editar_publicacion(self):
        # Crear una publicación de prueba
        publicacion = Publicacion.objects.create(
            titulo='Título de prueba',
            contenido='Contenido de prueba',
            imagen='publicaciones/test_image.jpg',
            creador=self.user
        )
        # Iniciar sesión como usuario
        self.client.login(username='prueba', password='contrasena1')
        response = self.client.get(reverse('pages:editar_publicacion', args=[publicacion.pk]))
        self.assertEqual(response.status_code, 200)
        form_data = {
            'titulo': 'Título editado',
            'contenido': 'Contenido editado',
            'imagen': 'publicaciones/test_image.jpg',
        }
        response = self.client.post(reverse('pages:editar_publicacion', args=[publicacion.pk]), form_data)
        self.assertRedirects(response, reverse('pages:detalle_publicacion', args=[publicacion.pk]))
        publicacion_actualizada = Publicacion.objects.get(pk=publicacion.pk)
        self.assertEqual(publicacion_actualizada.titulo, 'Título editado')
        self.assertEqual(publicacion_actualizada.contenido, 'Contenido editado')

    def test_eliminar_publicacion(self):
        # Crear una publicación de prueba
        publicacion = Publicacion.objects.create(
            titulo='Título de prueba',
            contenido='Contenido de prueba',
            imagen='publicaciones/test_image.jpg',
            creador=self.user
        )

        # Iniciar sesión como usuario
        self.client.login(username='prueba', password='contrasena1')
        response = self.client.post(reverse('pages:eliminar_publicacion', args=[publicacion.pk]))
        self.assertRedirects(response, reverse('pages:lista_publicaciones'))
        self.assertFalse(Publicacion.objects.filter(pk=publicacion.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'La publicación se ha eliminado correctamente.')

    def test_agregar_comentario(self):
        # Crear una publicación de prueba
        publicacion = Publicacion.objects.create(
            titulo='Título de prueba',
            contenido='Contenido de prueba',
            imagen='publicaciones/test_image.jpg',
            creador=self.user
        )
        self.client.login(username='prueba', password='contrasena1')
        url = reverse('pages:agregar_comentario', args=[publicacion.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Crear datos de prueba para el formulario de comentario
        form_data = {
            'contenido': 'Comentario de prueba',
        }
        response = self.client.post(url, form_data)
        self.assertRedirects(response, reverse('pages:detalle_publicacion', args=[publicacion.pk]))
        comentario = Comentario.objects.filter(publicacion=publicacion, autor=self.user).first()
        self.assertIsNotNone(comentario)
        self.assertEqual(comentario.contenido, 'Comentario de prueba')

    def test_eliminar_comentario(self):
        # Crear una publicación de prueba
        publicacion = Publicacion.objects.create(
            titulo='Título de prueba',
            contenido='Contenido de prueba',
            imagen='publicaciones/test_image.jpg',
            creador=self.user
        )
        # Crear un comentario de prueba
        comentario = Comentario.objects.create(
            publicacion=publicacion,
            autor=self.user,
            contenido='Comentario de prueba',
        )
        self.client.login(username='prueba', password='contrasena1')
        url = reverse('pages:eliminar_comentario', args=[comentario.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('pages:detalle_publicacion', args=[publicacion.pk]))
        self.assertFalse(Comentario.objects.filter(pk=comentario.pk).exists())

    def test_buscar_titulo(self):
        Publicacion.objects.create(
            titulo='Título de prueba',
            contenido='Contenido de prueba',
            imagen='publicaciones/test_image.jpg',
            creador=self.user
        )
        response = self.client.get(reverse('pages:buscar_titulo'), {'q': 'prueba'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Título de prueba")