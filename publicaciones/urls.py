from django.urls import path

from .views import listar_publicaciones, detalle_publicacion, crear_publicacion, EditarPublicacion, AgregarComentario

app_name = 'pages'

urlpatterns = [
    path('', listar_publicaciones, name='lista_publicaciones'),
    path('pages/<int:pk>/', detalle_publicacion, name='detalle_publicacion'),
    path('pages/crear/', crear_publicacion.as_view(), name='crear_publicacion'),
    path('pages/<int:pk>/editar/', EditarPublicacion.as_view(), name='editar_publicacion'),
    path('pages/<int:pk>/comentario/', AgregarComentario.as_view(), name='agregar_comentario'),
]