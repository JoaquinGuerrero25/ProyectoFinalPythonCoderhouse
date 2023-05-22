from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'perfil'

urlpatterns = [
    path('registro/', views.registrar_usuario, name='registro'),
    path('iniciar-sesion/', views.IniciarSesion.as_view(), name='login'),
    path('editar-usuario/', views.editar_usuario, name='editar_usuario'),
    path('agregar-avatar/', views.agregar_avatar, name='agregar_avatar'),
    path('mi-perfil/', views.ver_mi_perfil, name='mi_perfil'),
    path('perfil/<str:username>/', views.ver_perfil, name='ver_perfil'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('cambiar-contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)