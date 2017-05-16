from django.conf.urls import url, include
from django.contrib import admin
from apps.scout.views import *
from django.conf.urls.static import static
from django.contrib.auth.views import  password_reset, password_reset_done, \
    password_reset_confirm, password_reset_complete
from apps.usuario.views import index_view
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index_view, name='index'),
    url(r'^scout/', include('apps.scout.urls', namespace='scout')),
    url(r'^usuario/', include('apps.usuario.urls', namespace='usuario')),
    url(r'^reset/password_reset', password_reset,
        {'template_name': 'reset_password/password_reset_form.html',
         'email_template_name': 'reset_password/password_reset_email.html'},
        name='password_reset'),
    url(r'^password_reset_done', password_reset_done,
        {'template_name': 'reset_password/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm,
        {'template_name': 'reset_password/password_reset_confirm.html'},
        name='password_reset_confirm'
        ),
    url(r'^reset/done', password_reset_complete, {'template_name': 'reset_password/password_reset_complete.html'},
        name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)