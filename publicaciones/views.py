from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from .models import Publicacion, Comentario, EdicionPublicacion
from .forms import PublicacionForm, ComentarioForm, EdicionPublicacionForm


def listar_publicaciones(request):
    publicaciones = Publicacion.objects.all()
    if publicaciones:
        context = {'publicaciones': publicaciones}
    else:
        mensaje = 'No hay publicaciones creadas.'
        context = {'mensaje': mensaje}
    return render(request, 'publicaciones/listado_publicaciones.html', context)


def detalle_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    creador = publicacion.creador
    return render(request, 'publicaciones/detalle_publicacion.html', {'publicacion': publicacion, 'creador': creador})


class crear_publicacion(LoginRequiredMixin, CreateView):
    model = Publicacion
    form_class = PublicacionForm
    success_url = reverse_lazy('inicio')
    template_name = 'publicaciones/crear_publicacion.html'
    def form_valid(self, form):
        self.request.session['creador_pk'] = self.request.user.pk
        messages.success(self.request, 'La publicación se ha creado correctamente.')
        return super().form_valid(form)
    def get_success_url(self):
        return self.success_url


class EditarPublicacion(LoginRequiredMixin, UpdateView):
    model = EdicionPublicacion
    form_class = EdicionPublicacionForm
    template_name = 'publicaciones/editar_publicacion.html'

    def get_object(self, queryset=None):
        publicacion = get_object_or_404(Publicacion, pk=self.kwargs['pk'])
        edicion_publicacion, _ = EdicionPublicacion.objects.get_or_create(publicacion=publicacion)
        return edicion_publicacion

    def form_valid(self, form):
        form.instance.editor = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        publicacion = get_object_or_404(Publicacion, pk=self.kwargs['pk'])
        return reverse('pages:detalle_publicacion', args=[publicacion.pk])

    def dispatch(self, request, *args, **kwargs):
        publicacion = get_object_or_404(Publicacion, pk=self.kwargs['pk'])
        if request.user != publicacion.creador:
            return redirect('pages:detalle_publicacion', pk=publicacion.pk)
        return super().dispatch(request, *args, **kwargs)

class AgregarComentario(CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'publicaciones/agregar_comentario.html'

    def form_valid(self, form):
        publicacion = get_object_or_404(Publicacion, pk=self.kwargs['pk'])
        form.instance.publicacion = publicacion
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        publicacion = get_object_or_404(Publicacion, pk=self.kwargs['pk'])
        return reverse('pages:detalle_publicacion', args=[publicacion.pk])