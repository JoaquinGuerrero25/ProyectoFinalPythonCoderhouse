from django.urls import path
from .views import listar_publicaciones, detalle_publicacion, crear_publicacion, editar_publicacion, AgregarComentario, eliminar_publicacion, buscar_titulo, EliminarComentario
from django.conf import settings
from django.conf.urls.static import static

app_name = 'pages'

urlpatterns = [
    path('', listar_publicaciones, name='lista_publicaciones'),
    path('pages/<int:pk>/', detalle_publicacion, name='detalle_publicacion'),
    path('pages/crear/', crear_publicacion.as_view(), name='crear_publicacion'),
    path('pages/<int:pk>/editar/', editar_publicacion, name='editar_publicacion'),
    path('pages/<int:pk>/comentario/', AgregarComentario.as_view(), name='agregar_comentario'),
    path('eliminar_comentario/<int:pk>/', EliminarComentario.as_view(), name='eliminar_comentario'),
    path('eliminar/<int:pk>/', eliminar_publicacion, name='eliminar_publicacion'),
    path('buscar/titulo/', buscar_titulo, name='buscar_titulo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)