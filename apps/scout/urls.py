from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from apps.scout.views import principal_view, team_list, player_list, busqueda_avanzada, \
    add_player_to_squad, remove_player_from_squad, manage_squad, add_to_principals, remove_from_principals, \
    squad_edit, squad_list, add_like, remove_like, player_profile, autocomplete_search, search

urlpatterns = [
    url(r'^principal', login_required(principal_view), name='principal'),
    url(r'^busqueda_avanzada', login_required(busqueda_avanzada), name='busqueda_avanzada'),
    url(r'^team_list/(?P<championship_id>\d+)/$', login_required(team_list), name='team_list'),
    url(r'^player_list/(?P<team_id>\d+)/$', login_required(player_list), name='player_list'),
    url(r'^player/profile/(?P<player_id>\d+)/$', login_required(player_profile), name='player_profile'),
    url(r'^add_player_to_squad/(?P<player_id>\d+)/$', login_required(add_player_to_squad), name='add_player_to_squad'),
    url(r'^remove_player_from_squad/(?P<player_id>\d+)/$', login_required(remove_player_from_squad), name='remove_player_from_squad'),
    url(r'^manage_squad', login_required(manage_squad), name='manage_squad'),
    url(r'^squad_list', squad_list, name='squad_list'),
    url(r'^add_to_principals/(?P<player_id>\d+)/$', login_required(add_to_principals), name='add_to_principals'),
    url(r'^remove_from_principals/(?P<player_id>\d+)/$', login_required(remove_from_principals), name='remove_from_principals'),
    url(r'^squad_Edit', login_required(squad_edit), name='squad_edit'),
    url(r'^add_like/(?P<squad_id>\d+)/$', login_required(add_like), name='add_like'),
    url(r'^remove_like/(?P<squad_id>\d+)/$', login_required(remove_like), name='remove_like'),
    url(r'^autocomplete_search/', login_required(autocomplete_search), name='autocomplete_search'),
    url(r'^search/', search, name='search'),

]

