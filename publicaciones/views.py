from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from .models import Publicacion, Comentario, EdicionPublicacion
from .forms import PublicacionForm, ComentarioForm, Formulario_busqueda


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
    success_url = reverse_lazy('pages:lista_publicaciones')
    template_name = 'publicaciones/crear_publicacion.html'

    def form_valid(self, form):
        form.instance.creador = self.request.user
        messages.success(self.request, 'La publicación se ha creado correctamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return self.success_url

@login_required
def editar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk, creador=request.user)
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            EdicionPublicacion.objects.create(publicacion=publicacion, contenido=publicacion.contenido)
            return redirect('pages:detalle_publicacion', pk=publicacion.pk)
    else:
        form = PublicacionForm(instance=publicacion)
    return render(request, 'Publicaciones/editar_publicacion.html', {'form': form})


@login_required
def eliminar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk, creador=request.user)
    if request.method == 'POST':
        publicacion.delete()
        messages.success(request, 'La publicación se ha eliminado correctamente.')
        return redirect('pages:lista_publicaciones')
    else:
        return redirect('pages:lista_publicaciones')

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


def buscar_titulo(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if not query:
            mensaje = "Debe ingresar una palabra clave para buscar"
            return render(request, 'publicaciones/buscar_por_titulo.html', {'mensaje': mensaje})
        else:
            publicaciones = Publicacion.objects.filter(titulo__icontains=query)
            if publicaciones.exists():
                return render(request, 'publicaciones/resultado_busqueda.html', {'publicaciones': publicaciones})
            else:
                mensaje = f"No se encontraron publicaciones con la palabra clave '{query}' en el título"
                return render(request, 'publicaciones/buscar_por_titulo.html', {'mensaje': mensaje})