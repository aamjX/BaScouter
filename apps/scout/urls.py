from django.conf.urls import url
from apps.scout.views import principal_view, team_list, player_list, busqueda_avanzada, \
    add_player_to_squad, remove_player_from_squad, manage_squad, hacer_titular, hacer_suplente, \
    squad_edit, squad_list, addMeGusta, removeMeGusta, player_profile, autocomplete_search, search

urlpatterns = [
    url(r'^principal', principal_view, name='principal'),
    url(r'^busqueda_avanzada', busqueda_avanzada, name='busqueda_avanzada'),
    url(r'^team_list/(?P<championship_id>\d+)/$', team_list, name='team_list'),
    url(r'^player_list/(?P<team_id>\d+)/$', player_list, name='player_list'),
    url(r'^player/profile/(?P<player_id>\d+)/$', player_profile, name='player_profile'),
    url(r'^add_player_to_squad/(?P<player_id>\d+)/$', add_player_to_squad, name='add_player_to_squad'),
    url(r'^remove_player_from_squad/(?P<player_id>\d+)/$', remove_player_from_squad, name='remove_player_from_squad'),
    url(r'^manage_squad', manage_squad, name='manage_squad'),
    url(r'^squad_list', squad_list, name='squad_list'),
    url(r'^hacerTitular/(?P<jugador_id>\d+)/$', hacer_titular, name='hacerTitular'),
    url(r'^hacerSuplente/(?P<jugador_id>\d+)/$', hacer_suplente, name='hacerSuplente'),
    url(r'^squad_Edit', squad_edit, name='squad_edit'),
    url(r'^addMeGusta/(?P<alineacion_id>\d+)/$', addMeGusta, name='addMeGusta'),
    url(r'^removeMeGusta/(?P<alineacion_id>\d+)/$', removeMeGusta, name='removeMeGusta'),
    url(r'^autocomplete_search/', autocomplete_search, name='autocomplete_search'),
    url(r'^search/', search, name='search'),

]