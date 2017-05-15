from django.shortcuts import render, redirect, reverse
from apps.usuario.models import Profile, SearchValues, Comment
from apps.scout.models import Squad
from django.views.generic import CreateView, View
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from apps.usuario.forms import LoginForm, SignUpForm, CommentForm, ProfileUpdateForm, SearchValuesForm, UserUpdateForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from apps.scout.views import ordenarJugadores


def index_view(request):
    if request.method == 'POST':
        formulario = LoginForm(request.POST)
        if formulario.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('scout:principal')
    else:
        formulario = LoginForm()
    return render(request, 'index.html', {'formulario': formulario})

class SignUp(CreateView):
    model = User
    template_name = 'usuario/sing_up.html'
    form_class = SignUpForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(SignUp, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid() and request.POST.get('cbox2')=='True':
            user = form.save()
            searchValues = SearchValues.create(user)
            searchValues.save()
            profile = Profile.create(user)
            profile.image = '/static/img/perfil.png'
            profile.save()
            alineacion = Squad.create(user)
            alineacion.save()

            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, message="Debe aceptar los términos y condiciones"))

def comment_create(request, usuario_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.autor = request.user
            comment.user = User.objects.get(id=usuario_id)
            comment.save()
            return redirect(reverse('usuario:perfil', kwargs={'usuario_id':usuario_id})+'#comentarios')

    else:
        form = CommentForm()
    return render(request, 'usuario/editar_comentario.html', {'form':form, 'usuario_id':usuario_id})

def comment_edit(request, id_comment):
    comment = Comment.objects.get(id=id_comment)
    if request.method == 'GET':
        form = CommentForm(instance=comment)
    else:
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            if comment.autor.id == request.user.id:
                form.save()
                return redirect(reverse('usuario:perfil', kwargs={'usuario_id':comment.user.id})+'#comentarios')
            else:
                HttpResponse('Vista de errores')
    return render(request, 'usuario/editar_comentario.html', {'form':form, 'usuario_id':comment.user.id})

def comment_delete(request, id_comment):
    comment = Comment.objects.get(id=id_comment)
    if request.method == 'GET':
        if comment.user.id == request.user.id or comment.autor.id == request.user.id:
            comment.delete()
        return redirect(reverse('usuario:perfil', kwargs={'usuario_id':comment.user.id})+'#comentarios')
    else:
        return redirect('error')

def UserList(request):
    usuarios = User.objects.all()
    return render(request, 'usuario/user_list.html', {'usuarios':usuarios})


def follow_user(request, usuario_id):
    if request.method == 'GET' and User.objects.filter(id=usuario_id).exists():
        user = User.objects.get(id=usuario_id)
        principal = request.user
        if principal.id != user.id:
            principal.profile.following.add(user)
            user.profile.followed_by.add(request.user)
        return redirect(reverse('usuario:perfil', kwargs={'usuario_id':usuario_id}))

    else:
        return redirect('usuario:list')

def unfollow_user(request, usuario_id):
    if request.method == 'GET' and User.objects.filter(id=usuario_id).exists():
        user = User.objects.get(id=usuario_id)
        principal = request.user
        if principal.id != user.id:
            principal.profile.following.remove(user)
            user.profile.followed_by.remove(request.user)
        return redirect('usuario:list')

    else:
        return redirect('usuario:list')

def following_list(request, usuario_id):
    user = User.objects.get(id=usuario_id)
    usuarios = user.profile.following.all()
    return render(request, 'usuario/user_list.html', {'usuarios':usuarios})

def followers_list(request, usuario_id):
    user = User.objects.get(id=usuario_id)
    usuarios = user.profile.followed_by.all()
    return render(request, 'usuario/user_list.html', {'usuarios': usuarios})


def perfil(request, usuario_id):
    user = User.objects.get(id=usuario_id)
    titulares_id = []
    siguiendo_id = []
    seguidores_id = []
    alineacion = Squad.objects.get(user=user)
    jugadores_ordenados = ordenarJugadores(alineacion.jugadores.all())
    comments = Comment.objects.filter(user=user)

    for t in alineacion.titulares.all():
        titulares_id.append(t.id)

    for u in user.profile.followed_by.all():
        seguidores_id.append(u.id)

    for u in user.profile.following.all():
        siguiendo_id.append(u.id)

    return render(request, 'usuario/perfil.html', {'user': user, 'alineacion': alineacion, 'porteros': jugadores_ordenados['porteros'],
                   'defensas': jugadores_ordenados['defensas'], 'medios': jugadores_ordenados['medios'],
                   'delanteros': jugadores_ordenados['delanteros'],
                   'titulares_id': titulares_id,'comments':comments, 'siguiendo_id': siguiendo_id, 'seguidores_id':seguidores_id})


def editarBusqueda(request):
    searchValues = SearchValues.objects.get(user=request.user)
    if request.method == 'GET':
        form = SearchValuesForm(instance=searchValues)
    else:
        form = SearchValuesForm(request.POST, instance=searchValues)
        if form.is_valid():
            form.save()
        return redirect('scout:busqueda_avanzada')
    return render(request, 'usuario/search_values_edit.html', {'form': form})


class ProfileVIew(View):

    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'usuario/editar_perfil.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'usuario_id':request.user.id
        })

    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(reverse('usuario:perfil', kwargs={'usuario_id':request.user.id}))


