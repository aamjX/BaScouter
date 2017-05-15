from django.conf.urls import url
from apps.scout.views import principal_view, team_list, player_list, busqueda_avanzada, \
    add_jugador_alineacion, remove_jugador_alineacion, gestionar_alineacion, hacer_titular, hacer_suplente, \
    editar_alineacion, listar_alineaciones, addMeGusta, removeMeGusta, player_profile, autocomplete_search, search

urlpatterns = [
    url(r'^principal', principal_view, name='principal'),
    url(r'^busqueda_avanzada', busqueda_avanzada, name='busqueda_avanzada'),
    url(r'^team_list/(?P<championship_id>\d+)/$', team_list, name='team_list'),
    url(r'^player_list/(?P<team_id>\d+)/$', player_list, name='player_list'),
    url(r'^player/profile/(?P<player_id>\d+)/$', player_profile, name='player_profile'),
    url(r'^jugadorAdd/(?P<jugador_id>\d+)/$', add_jugador_alineacion, name='addJugador'),
    url(r'^jugadorRemove/(?P<jugador_id>\d+)/$', remove_jugador_alineacion, name='removeJugador'),
    url(r'^gestionar_alineacion', gestionar_alineacion, name='gestionar_alineacion'),
    url(r'^listar_alineaciones', listar_alineaciones, name='listar_alineaciones'),
    url(r'^hacerTitular/(?P<jugador_id>\d+)/$', hacer_titular, name='hacerTitular'),
    url(r'^hacerSuplente/(?P<jugador_id>\d+)/$', hacer_suplente, name='hacerSuplente'),
    url(r'^editarAlineaciaon', editar_alineacion, name='editarAlineacion'),
    url(r'^addMeGusta/(?P<alineacion_id>\d+)/$', addMeGusta, name='addMeGusta'),
    url(r'^removeMeGusta/(?P<alineacion_id>\d+)/$', removeMeGusta, name='removeMeGusta'),
    url(r'^autocomplete_search/', autocomplete_search, name='autocomplete_search'),
    url(r'^search/', search, name='search'),

]