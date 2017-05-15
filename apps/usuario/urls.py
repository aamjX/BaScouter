from django.conf.urls import url
from django.contrib.auth.views import logout, password_change, password_change_done
from apps.usuario.views import SignUp, perfil, editarBusqueda, ProfileVIew, comment_create, comment_delete, \
    comment_edit, UserList, follow_user, unfollow_user, following_list, followers_list

urlpatterns = [
    url(r'^registrar', SignUp.as_view(), name="registrar"),
    url(r'^perfil/(?P<usuario_id>\d+)/$', perfil, name="perfil"),
    url(r'^perfil/editar/$', ProfileVIew.as_view(), name="editarPerfil"),
    url(r'^listar/$', UserList, name="list"),
    url(r'^siguiendo/listar/(?P<usuario_id>\d+)$', following_list, name="following"),
    url(r'^seguidores/listar/(?P<usuario_id>\d+)$', followers_list, name="followers"),
    url(r'^perfil/editarBusqueda/$', editarBusqueda, name="editarBusqueda"),
    url(r'^logout/$', logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^comment_create/(?P<usuario_id>\d+)$', comment_create, name='comment_create'),
    url(r'^comment_edit/(?P<id_comment>\d+)$', comment_edit, name='comment_edit'),
    url(r'^comment_delete/(?P<id_comment>\d+)$', comment_delete, name='comment_delete'),
    url(r'^follow_user/(?P<usuario_id>\d+)$', follow_user, name='follow'),
    url(r'^unfollow_user/(?P<usuario_id>\d+)$', unfollow_user, name='unfollow'),
    url(r'^password_change$', password_change, name='password_change', kwargs={
        'template_name': 'usuario/password_change_form.html',
        'post_change_redirect': 'usuario:password_change_done',
    }
        ),
    url(r'^password_change_done$', password_change_done,
        name='password_change_done',
        kwargs={'template_name': 'usuario/password_change_done.html'}
        ),


]