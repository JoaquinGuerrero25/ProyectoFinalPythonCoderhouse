from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import RegistroForm, EditarUsuarioForm, AgregarAvatarForm
from .models import Avatar
from publicaciones.models import Publicacion

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('pages:lista_publicaciones')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})


class IniciarSesion(LoginView):
    template_name = 'usuarios/iniciar_sesion.html'
    redirect_authenticated_user = True
    success_url = 'pages:lista_publicaciones'

    def form_invalid(self, form):
        messages.error(self.request, 'El nombre de usuario o la contraseña son incorrectos.')
        return super().form_invalid(form)


@login_required
def editar_usuario(request):
    user = request.user
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('perfil:mi_perfil')
    else:
        form = EditarUsuarioForm(instance=user)
    return render(request, 'usuarios/editar_usuario.html', {'form': form})


@login_required
def cambiar_contrasena(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('perfil:mi_perfil')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'usuarios/cambiar_contrasena.html', {'form': form})


@login_required
def agregar_avatar(request):
    user = request.user
    try:
        avatar = Avatar.objects.get(user=user)
    except Avatar.DoesNotExist:
        avatar = Avatar(user=user)
    if request.method == 'POST':
        form = AgregarAvatarForm(request.POST, request.FILES, instance=avatar)
        if form.is_valid():
            form.save()
            return redirect('perfil:mi_perfil')
    else:
        form = AgregarAvatarForm(instance=avatar)
    return render(request, 'usuarios/agregar_avatar.html', {'form': form})


@login_required
def ver_mi_perfil(request):
    user = request.user
    publicaciones = Publicacion.objects.filter(creador=user)
    try:
        avatar = Avatar.objects.get(user=user)
    except ObjectDoesNotExist:
        avatar = None
    context = {
        'avatar': avatar,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'publicaciones':publicaciones,
    }
    return render(request, 'usuarios/perfil.html', context)


def ver_perfil(request, username):
    user = get_object_or_404(User, username=username)
    avatar = Avatar.objects.get(user=user)
    publicaciones = Publicacion.objects.filter(creador=user)
    context = {
        'avatar': avatar,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'publicaciones':publicaciones,
    }
    return render(request, 'usuarios/perfil_autor.html', context)


def cerrar_sesion(request):
    logout(request)
    return redirect('pages:lista_publicaciones')


def acerca_de_mi(request):
    return render(request, 'usuarios/acerca_de_mi.html')