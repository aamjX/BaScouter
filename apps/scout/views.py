from apps.scout.utils import ratingCalculte, favAlineaciones_ID_ByUser, ordenarJugadores
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.db.models import Q
from apps.scout.models import Championship, Team, Player, Squad, Like
from apps.scout.forms import BusquedaAvanzadaForm, SquadForm
from django.contrib.auth.models import User
import time
import json
from django.shortcuts import render_to_response
from django.template import RequestContext

'''----------------------------------------------------------------------------------------------------------'''

'''Vista principal una vez autenticado'''

'''----------------------------------------------------------------------------------------------------------'''


def principal_view(request):
    championships = Championship.objects.all()
    return render(request, 'scout/principal.html', {'championships': championships})


'''----------------------------------------------------------------------------------------------------------'''

'''Listar entidades'''

'''----------------------------------------------------------------------------------------------------------'''


def team_list(request, championship_id):

    if Championship.objects.filter(id=championship_id).exists():

        championship = Championship.objects.get(pk=championship_id)
        teamsCount = len(championship.team_set.all())
        playerCount = 0
        value = 0

        for team in championship.team_set.all():
            playerCount = playerCount + len(team.player_set.all())

        for team in championship.team_set.all():
            value = value + team.value

        teams = Team.objects.filter(championship=championship)
        return render(request, 'scout/team_list.html',
                      {'teams': teams, 'championship': championship, 'teamsCount': teamsCount, 'playerCount': playerCount,
                       'value': value})

    else:

        return render(request, 'error/error_1.html')



def player_list(request, team_id):

    if Player.objects.filter(id=team_id):

        players_id = []
        team = Team.objects.get(pk=team_id)
        squad = Squad.objects.get(user=request.user)
        for player in squad.players.all():
            players_id.append(player.id)
        return render(request, 'scout/player_list.html',
                      {'players': team.player_set.all(), 'team': team, 'players_id': players_id})
    else:

        return render(request, 'error/error_1.html')



def squad_list(request):
    squads = Squad.objects.all()
    sorted_squads = []
    sorted_squad_single = []
    sqd = []
    for a in squads:
        principals = ordenarJugadores(a.principals.all())
        for t in principals['porteros']:
            sorted_squad_single.append(t)
        for t in principals['defensas']:
            sorted_squad_single.append(t)
        for t in principals['medios']:
            sorted_squad_single.append(t)
        for t in principals['delanteros']:
            sorted_squad_single.append(t)

        sorted_squads.append(sorted_squad_single)
        sqd.append(a)
        sorted_squad_single = []
        list_all = zip(sqd, sorted_squads)
        squads_id = favAlineaciones_ID_ByUser(request.user)
    return render(request, 'scout/squad_list.html',
                  {'squads': list_all, 'squads_id': squads_id})


'''----------------------------------------------------------------------------------------------------------'''

'''Mostrar entidades'''

'''----------------------------------------------------------------------------------------------------------'''


def player_profile(request, player_id):
    if Player.objects.filter(id=player_id).exists():

        player = Player.objects.get(id=player_id)
        players_id = []

        squad = Squad.objects.get(user=request.user)

        for p in squad.players.all():
            players_id.append(p.id)

        return render(request, 'scout/player_profile.html', {'player': player, 'players_id': players_id})

    else:
        return render(request, 'error/error_1.html')


'''----------------------------------------------------------------------------------------------------------'''

'''Funciones relacionadas con el manego de las alineaciones'''

'''----------------------------------------------------------------------------------------------------------'''

def manage_squad(request):
    principals_id = []
    players_id = []
    principals_value = 0
    average_age = 0
    user = request.user
    squad = Squad.objects.get(user=user)

    sorted_players = ordenarJugadores(squad.players.all())
    for j in squad.players.all():
        players_id.append(j.id)

    for t in squad.principals.all():
        principals_value = principals_value + t.value
        average_age = average_age + t.age
        principals_id.append(t.id)

    if len(squad.principals.all()) != 0:
        average_age = average_age / len(squad.principals.all())

    squad.value = principals_value
    squad.averageAge = int(average_age)
    squad.save()

    return render(request, 'scout/manage_squad.html',
                  {'squad': squad, 'porteros': sorted_players['porteros'],
                   'defensas': sorted_players['defensas'], 'medios': sorted_players['medios'],
                   'delanteros': sorted_players['delanteros'], 'players_id': players_id,
                   'principals_id': principals_id, 'principals_value': principals_value,
                   'average_age': int(average_age)})


def squad_edit(request):
    squad = Squad.objects.get(user=request.user)
    if request.method == 'GET':
        form = SquadForm(instance=squad)
    else:
        form = SquadForm(request.POST, instance=squad)
        if form.is_valid():
            form.save()
            return redirect('scout:manage_squad')
        else:
            return render(request, 'scout/squad_edit.html', {'form': form})

    return render(request, 'scout/squad_edit.html', {'form': form})


def add_player_to_squad(request, player_id):
    if Player.objects.filter(id=player_id).exists():
        user = request.user
        squad = Squad.objects.get(user=user)
        player = Player.objects.get(id=player_id)
        team = player.team
        squad.players.add(player)
        return render(request, 'scout/congratulations.html', {'team': team, 'player': player, 'isAdd': True})
    else:
        return render(request, 'error/error_1.html')


def remove_player_from_squad(request, player_id):
    if Player.objects.filter(id=player_id).exists():
        user = request.user
        squad = Squad.objects.get(user=user)
        player = Player.objects.get(id=player_id)
        team = player.team
        squad.players.remove(player)
        if player in squad.principals.all():
            squad.principals.remove(player)
        return render(request, 'scout/congratulations.html', {'team': team, 'player': player, 'isAdd': False})
    else:
        return render(request, 'error/error_1.html')


def add_to_principals(request, player_id):
    if Player.objects.filter(id=player_id).exists():

        user = request.user
        squad = Squad.objects.get(user=user)
        player = Player.objects.get(id=player_id)
        squad.principals.add(player)
        now = time.strftime("%Y-%m-%d")
        squad.lastUpdate = now
        squad.save()
        likes = Like.objects.all().filter(squad=squad)
        for l in likes:
            l.delete()
        if player.likes == None:
            player.likes = 0
        player.likes += 1
        player.save()
        return redirect('scout:manage_squad')

    else:

        return render(request, 'error/error_1.html')


def remove_from_principals(request, player_id):
    if Player.objects.filter(id=player_id).exists():
        user = request.user
        squad = Squad.objects.get(user=user)
        player = Player.objects.get(id=player_id)
        squad.principals.remove(player)
        now = time.strftime("%Y-%m-%d")
        squad.lastUpdate = now
        squad.save()
        likes = Like.objects.all().filter(squad=squad)
        for l in likes:
            l.delete()
        player.likes -= 1
        player.save()

        return redirect('scout:manage_squad')

    else:
        return render(request, 'error/error_1.html')


'''----------------------------------------------------------------------------------------------------------'''

'''Funciones relacionadas con la popularidad'''

'''----------------------------------------------------------------------------------------------------------'''


def add_like(request, squad_id):
    if Squad.objects.filter(id=squad_id).exists():
        squad = Squad.objects.get(id=squad_id)
        if not Like.objects.filter(user=request.user, squad=squad).exists():
            like = Like.create(request.user, squad)
            squad.likeCount += 1
            squad.save()
            like.save()
        return redirect(reverse('scout:squad_list') + '#alineacion' + str(squad.id))
    else:
        return render(request, 'error/error_1.html')


def remove_like(request, squad_id):
    if Squad.objects.filter(id=squad_id).exists():
        squad = Squad.objects.get(id=squad_id)
        user = request.user
        if Like.objects.filter(user=user, squad=squad).exists():
            like = Like.objects.get(user=user, squad=squad)
            if like.user == request.user:
                like.delete()
                squad.likeCount -= 1
                squad.save()

            return redirect(reverse('scout:squad_list') + '#alineacion' + str(squad.id))
        else:
            return render(request, 'error/error_1.html')
    else:
        return render(request, 'error/error_1.html')


'''----------------------------------------------------------------------------------------------------------'''

'''Funciones relacionadas con el sistema de busqueda'''

'''----------------------------------------------------------------------------------------------------------'''


def busqueda_avanzada(request):
    if request.method == 'POST':
        formulario = BusquedaAvanzadaForm(request.POST)
        if formulario.is_valid():
            competicion = formulario.cleaned_data['competicion']
            nacionalidades = formulario.cleaned_data['nacionalidad']
            alias = formulario.cleaned_data['alias']
            nombreCompleto = formulario.cleaned_data['nombreCompleto']
            posiciones = formulario.cleaned_data['posicion']
            dorsal = formulario.cleaned_data['dorsal']
            mayor_de = formulario.cleaned_data['mayor_de']
            menor_de = formulario.cleaned_data['menor_de']
            mayor_valor_de = formulario.cleaned_data['mayor_valor_de']
            menor_valor_de = formulario.cleaned_data['menor_valor_de']
            mayor_altura_de = formulario.cleaned_data['mayor_altura_de']
            menor_altura_de = formulario.cleaned_data['menor_altura_de']
            pie = formulario.cleaned_data['pie']
            contratoHasta = formulario.cleaned_data['contratoHasta']
            fichado = formulario.cleaned_data['fichado']
            agentes = formulario.cleaned_data['agente']
            proveedores = formulario.cleaned_data['proveedor']
            temporada = formulario.cleaned_data['temporada']
            utilizarRating = formulario.cleaned_data['utilizarRating']

            query_fichado = Q()
            query_nacionalidad = Q()
            query_posicion = Q()
            query_contratoHasta = Q()
            query_agente = Q()
            query_proveedor = Q()
            query_pie = Q()

            if pie != 'Cualquiera':
                query_pie = query_pie | Q(foot=pie)
            if fichado != None:
                query_fichado = query_fichado | Q(inTheTeamSince__year=fichado)
            if contratoHasta != None:
                query_contratoHasta = query_contratoHasta | Q(contractUntil__year=contratoHasta)
            for nacionalidad in nacionalidades:
                query_nacionalidad = query_nacionalidad | Q(nationality__icontains=nacionalidad)
            for posicion in posiciones:
                query_posicion = query_posicion | Q(position__icontains=posicion)
            for agente in agentes:
                query_agente = query_agente | Q(agent__icontains=agente)
            for proveedor in proveedores:
                query_proveedor = query_proveedor | Q(outfitter__icontains=proveedor)

            if dorsal == None:
                jugadores = Player.objects.filter(query_agente, query_proveedor, query_nacionalidad, query_posicion,
                                                  query_contratoHasta, query_fichado, query_pie,
                                                  team__championship__id=competicion,
                                                  name__icontains=alias, fullName__icontains=nombreCompleto,
                                                  height__range=(mayor_altura_de, menor_altura_de),
                                                  birthDate__range=(mayor_de, menor_de),
                                                  value__range=(mayor_valor_de, menor_valor_de))
            else:
                jugadores = Player.objects.filter(query_agente, query_proveedor, query_nacionalidad, query_posicion,
                                                  query_contratoHasta, query_fichado, query_pie,
                                                  team__championship__id=competicion,
                                                  name__icontains=alias, fullName__icontains=nombreCompleto,
                                                  number=dorsal, height__range=(mayor_altura_de, menor_altura_de),
                                                  birthDate__range=(mayor_de, menor_de),
                                                  value__range=(mayor_valor_de, menor_valor_de))

            if utilizarRating:
                jugadores = ratingCalculte(jugadores, request.user, temporada)

            ids_jugadores = []

            alineacion = Squad.objects.get(user=request.user)
            for j in alineacion.players.all():
                ids_jugadores.append(j.id)

            return render(request, 'scout/avanced_search_result.html',
                          {'jugadores': jugadores, 'utilizarRating': utilizarRating, 'ids_jugadores': ids_jugadores})
    else:
        formulario = BusquedaAvanzadaForm()
    return render(request, 'scout/advanced_search.html', {'formulario': formulario})


def autocomplete_search(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        equipos = Team.objects.filter(name__icontains=q)[:5]
        usuarios = User.objects.filter(username__icontains=q)[:5]
        jugadores = Player.objects.filter(name__icontains=q)[:5]
        results = []
        for equipo in equipos:
            datos_json = {}
            datos_json['id'] = equipo.id
            datos_json[
                'label'] = equipo.name
            datos_json['img'] = equipo.badge
            datos_json['value'] = equipo.name
            results.append(datos_json)

        for jugador in jugadores:
            datos_json = {}
            datos_json['id'] = jugador.id
            datos_json[
                'label'] = jugador.name
            datos_json['img'] = jugador.image
            datos_json['value'] = jugador.name
            results.append(datos_json)

        for usuario in usuarios:
            datos_json = {}
            datos_json['id'] = usuario.id
            datos_json[
                'label'] = usuario.username + ' <i class ="fa fa-heart" aria-hidden="true" style = "color: #F95959; font-size: 12px"></i> ' + str(usuario.squad.likeCount)
            datos_json['img'] = usuario.profile.image.url
            datos_json['value'] = usuario.username
            results.append(datos_json)


        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def search(request):
    if request.method == 'GET':
        key = request.GET['key']
        if Team.objects.filter(name=key).exists():
            equipo = Team.objects.get(name=key)
            return redirect(reverse('scout:player_list', kwargs={'team_id': equipo.id}))
        elif User.objects.filter(username=key).exists():
            usuario = User.objects.get(username=key)
            return redirect(reverse('usuario:profile', kwargs={'user_id': usuario.id}))
        elif Player.objects.filter(name=key).exists():
            player = Player.objects.get(name=key)
            return redirect(reverse('scout:player_profile', kwargs={'player_id': player.id}))
        else:
            equipos = Team.objects.filter(name__icontains=key)
            usuarios = User.objects.filter(username__icontains=key)
            jugadores = Player.objects.filter(name__icontains=key)

            return render(request, 'scout/search_result.html',
                          {'equipos': equipos, 'usuarios': usuarios, 'jugadores': jugadores, 'key_word': key})
    else:

        return render(request, 'error/error_1.html')



'''----------------------------------------------------------------------------------------------------------'''

'''Personalizando vista de errores'''

'''----------------------------------------------------------------------------------------------------------'''


def handler404(request):
    response = render(request, 'error/404.html')
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, 'error/500.html')
    response.status_code = 500
    return response


