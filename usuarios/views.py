from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistroForm, EditarUsuarioForm, AgregarAvatarForm
from .models import Avatar


def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})


class IniciarSesion(LoginView):
    template_name = 'iniciar_sesion.html'
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
            return redirect('perfil')
    else:
        form = EditarUsuarioForm(instance=user)
    return render(request, 'editar_usuario.html', {'form': form})


@login_required
def agregar_avatar(request):
    user = request.user
    if request.method == 'POST':
        form = AgregarAvatarForm(request.POST, request.FILES, instance=user.avatar)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = AgregarAvatarForm()
    return render(request, 'agregar_avatar.html', {'form': form})


@login_required
def ver_mi_perfil(request):
    user = request.user
    avatar = Avatar.objects.get(user=user)
    context = {
        'avatar': avatar,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }
    return render(request, 'perfil.html', context)


def ver_perfil(request, username):
    user = get_object_or_404(User, username=username)
    avatar = Avatar.objects.get(user=user)
    context = {
        'avatar': avatar,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }
    return render(request, 'perfil.html', context)