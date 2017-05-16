from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout, password_change, password_change_done
from apps.usuario.views import SignUp, profile, editarBusqueda, ProfileView, comment_create, comment_delete, \
    comment_edit, UserList, follow_user, unfollow_user, following_list, followers_list


urlpatterns = [
    url(r'^registrar', SignUp.as_view(), name="registrar"),
    url(r'^profile/(?P<user_id>\d+)/$', login_required(profile), name="profile"),
    url(r'^profile/edit/$', login_required(ProfileView.as_view()), name="user_profile_edit"),
    url(r'^user_list/$', login_required(UserList), name="user_list"),
    url(r'^siguiendo/listar/(?P<usuario_id>\d+)$', login_required(following_list), name="following"),
    url(r'^seguidores/listar/(?P<usuario_id>\d+)$', login_required(followers_list), name="followers"),
    url(r'^perfil/editarBusqueda/$', login_required(editarBusqueda), name="editarBusqueda"),
    url(r'^logout/$', login_required(logout), name='logout', kwargs={'next_page': '/'}),
    url(r'^comment_create/(?P<usuario_id>\d+)$', login_required(comment_create), name='comment_create'),
    url(r'^comment_edit/(?P<id_comment>\d+)$', login_required(comment_edit), name='comment_edit'),
    url(r'^comment_delete/(?P<id_comment>\d+)$', login_required(comment_delete), name='comment_delete'),
    url(r'^follow_user/(?P<usuario_id>\d+)$', login_required(follow_user), name='follow'),
    url(r'^unfollow_user/(?P<usuario_id>\d+)$', login_required(unfollow_user), name='unfollow'),
    url(r'^password_change$', login_required(password_change), name='password_change', kwargs={
        'template_name': 'usuario/password_change_form.html',
        'post_change_redirect': 'usuario:password_change_done',
    }
        ),
    url(r'^password_change_done$', login_required(password_change_done),
        name='password_change_done',
        kwargs={'template_name': 'usuario/password_change_done.html'}
        ),


]