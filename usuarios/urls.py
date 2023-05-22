from django.urls import path
from . import views

app_name = 'perfil'

urlpatterns = [
    path('registro/', views.registrar_usuario, name='registro'),
    path('iniciar-sesion/', views.IniciarSesion.as_view(), name='iniciar_sesion'),
    path('editar-usuario/', views.editar_usuario, name='editar_usuario'),
    path('agregar-avatar/', views.agregar_avatar, name='agregar_avatar'),
    path('mi-perfil/', views.ver_mi_perfil, name='mi_perfil'),
    path('perfil/<str:username>/', views.ver_perfil, name='ver_perfil'),
]