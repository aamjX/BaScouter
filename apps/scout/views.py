from django.shortcuts import render, redirect, reverse, HttpResponse
from django.db.models import Q
from apps.scout.models import Championship, Team, Performance, Player, Squad, Like
from apps.usuario.models import SearchValues
from apps.scout.forms import BusquedaAvanzadaForm, SquadForm
from django.contrib.auth.models import User
import time
import json


'''Vista principal una vez autenticado'''

def principal_view(request):
    championships = Championship.objects.all()
    return render(request, 'scout/principal.html', {'championships': championships})


'''Listar entidades'''

def team_list(request, championship_id):
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

def player_list(request, team_id):
    players_id = []
    team = Team.objects.get(pk=team_id)
    squad = Squad.objects.get(user=request.user)
    for player in squad.players.all():
        players_id.append(player.id)
    return render(request, 'scout/player_list.html',
                  {'players': team.player_set.all(), 'team': team, 'players_id': players_id})


'''Mostrar entidades'''

def player_profile(request, player_id):
    player = Player.objects.get(id=player_id)
    players_id = []

    squad = Squad.objects.get(user=request.user)
    for player in squad.players.all():
        players_id.append(player.id)

    return render(request, 'scout/player_profile.html', {'player': player, 'players_id': players_id})




def add_jugador_alineacion(request, jugador_id):
    user = request.user
    alineacion = Squad.objects.get(user=user)
    jugador = Team.objects.get(id=jugador_id)
    equipo = jugador.equipo
    alineacion.jugadores.add(jugador)
    return render(request, 'scout/enhorabuena.html', {'equipo': equipo, 'jugador': jugador, 'isAdd': True})


def remove_jugador_alineacion(request, jugador_id):
    user = request.user
    alineacion = Squad.objects.get(user=user)
    jugador = Player.objects.get(id=jugador_id)
    equipo = jugador.equipo
    alineacion.jugadores.remove(jugador)
    if jugador in alineacion.titulares.all():
        alineacion.titulares.remove(jugador)
    return render(request, 'scout/enhorabuena.html', {'equipo': equipo, 'jugador': jugador, 'isAdd': False})


def hacer_titular(request, jugador_id):
    user = request.user
    alineacion = Squad.objects.get(user=user)
    jugador = Player.objects.get(id=jugador_id)
    alineacion.titulares.add(jugador)
    now = time.strftime("%Y-%m-%d")
    alineacion.ultimaActualizacion = now
    alineacion.save()
    meGustas = Like.objects.all().filter(squad=alineacion)
    for mG in meGustas:
        mG.delete()
    jugador.popularidad += 1
    jugador.save()
    return redirect('scout:gestionar_alineacion')


def hacer_suplente(request, jugador_id):
    user = request.user
    alineacion = Squad.objects.get(user=user)
    jugador = Player.objects.get(id=jugador_id)
    alineacion.titulares.remove(jugador)
    now = time.strftime("%Y-%m-%d")
    alineacion.ultimaActualizacion = now
    alineacion.save()
    meGustas = Like.objects.all().filter(squad=alineacion)
    for mG in meGustas:
        mG.delete()
    jugador.popularidad -= 1
    return redirect('scout:gestionar_alineacion')


def gestionar_alineacion(request):
    titulares_id = []
    jugadores_id = []
    valor_titulares = 0
    edad_media = 0
    user = request.user
    alineacion = Squad.objects.get(user=user)

    jugadores_ordenados = ordenarJugadores(alineacion.jugadores.all())
    for j in alineacion.jugadores.all():
        jugadores_id.append(j.id)

    for t in alineacion.titulares.all():
        valor_titulares = valor_titulares + t.valor
        edad_media = edad_media + t.edad
        titulares_id.append(t.id)

    if len(alineacion.titulares.all()) != 0:
        edad_media = edad_media / len(alineacion.titulares.all())

    alineacion.valor = valor_titulares
    alineacion.edadMedia = int(edad_media)
    alineacion.save()

    return render(request, 'scout/gestionar_alineacion.html',
                  {'alineacion': alineacion, 'porteros': jugadores_ordenados['porteros'],
                   'defensas': jugadores_ordenados['defensas'], 'medios': jugadores_ordenados['medios'],
                   'delanteros': jugadores_ordenados['delanteros'], 'jugadores_id': jugadores_id,
                   'titulares_id': titulares_id, 'valor_titulres': valor_titulares, 'edad_media': int(edad_media)})


def editar_alineacion(request):
    alineacion = Squad.objects.get(user=request.user)
    if request.method == 'GET':
        form = SquadForm(instance=alineacion)
    else:
        form = SquadForm(request.POST, instance=alineacion)
        if form.is_valid():
            form.save()
        return redirect('scout:gestionar_alineacion')
    return render(request, 'scout/squad_edit.html', {'form': form})


def listar_alineaciones(request):
    alineaciones = Squad.objects.all()
    alineaciones_ordenadas = []
    alineacion_ordenada = []
    ali = []
    for a in alineaciones:
        titulares = ordenarJugadores(a.titulares.all())
        for t in titulares['porteros']:
            alineacion_ordenada.append(t)
        for t in titulares['defensas']:
            alineacion_ordenada.append(t)
        for t in titulares['medios']:
            alineacion_ordenada.append(t)
        for t in titulares['delanteros']:
            alineacion_ordenada.append(t)
        alineaciones_ordenadas.append(alineacion_ordenada)
        ali.append(a)
        alineacion_ordenada = []
        list_all = zip(ali, alineaciones_ordenadas)
        alineaciones_id = favAlineaciones_ID_ByUser(request.user)
    return render(request, 'scout/listar_alineaciones.html',
                  {'alineaciones': list_all, 'alineaciones_id': alineaciones_id})


def addMeGusta(request, alineacion_id):
    alineacion = Squad.objects.get(id=alineacion_id)
    if not Like.objects.filter(user=request.user, squad=alineacion).exists():
        mG = Like.create(request.user, alineacion)
        alineacion.likeCount += 1
        alineacion.save()
        mG.save()
    return redirect(reverse('scout:listar_alineaciones') + '#alineacion' + str(alineacion.id))


def removeMeGusta(request, alineacion_id):
    alineacion = Squad.objects.get(id=alineacion_id)
    user = request.user
    meGusta = Like.objects.get(user=user, squad=alineacion)
    if meGusta.user == request.user:
        meGusta.delete()
        alineacion.likeCount -= 1
        alineacion.save()

        return redirect(reverse('scout:listar_alineaciones') + '#alineacion' + str(alineacion.id))


def favAlineaciones_ID_ByUser(principal_user):
    alinaciones_id = []
    user = principal_user
    user_meGustas = Like.objects.all().filter(user=user)

    for uMG in user_meGustas:
        alinaciones_id.append(uMG.alineacion.id)

    return alinaciones_id

'''Funciones relacionadas con el sistema de busqueda'''

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
                                                   height__range =(mayor_altura_de, menor_altura_de),
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
    return render(request, 'scout/busqueda_avanzada.html', {'formulario': formulario})


def autocomplete_search(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        equipos = Player.objects.filter(name__icontains=q)[:8]
        usuarios = User.objects.filter(username__icontains=q)[:8]
        results = []
        for equipo in equipos:
            datos_json = {}
            datos_json['id'] = equipo.id
            datos_json[
                'label'] = equipo.name + ' | <i class="fa fa-futbol-o" aria-hidden="true" style="font-size:12px"></i>'
            datos_json['img'] = equipo.badge
            datos_json['value'] = equipo.name
            results.append(datos_json)

        for usuario in usuarios:
            datos_json = {}
            datos_json['id'] = usuario.id
            datos_json['label'] = usuario.username + ' | <i class ="fa fa-heart" aria-hidden="true" style = "color: #F95959; font-size: 12px"></i> ' + str(
                usuario.squad.likeCount)
            datos_json['img'] = usuario.profile.image
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
            return redirect(reverse('scout:equipo', kwargs={'equipo_id': equipo.id}))
        elif User.objects.filter(username=key).exists():
            usuario = User.objects.get(username=key)
            return redirect(reverse('usuario:perfil', kwargs={'usuario_id': usuario.id}))
        else:
            equipos = Team.objects.filter(name__icontains=key)
            usuarios = User.objects.filter(username__icontains=key)

            return render(request, 'scout/search_result.html',
                          {'equipos': equipos, 'usuarios': usuarios, 'key_word': key})

    return redirect('scout:principal')

'''Funciones auxiliares'''


def ordenarJugadores(jugadores):
    porteros = []
    defensas = []
    medios = []
    delanteros = []

    for jugador in jugadores:
        if 'Portero' in jugador.posicion:
            porteros.append(jugador)
        elif 'Defensa' in jugador.posicion:
            defensas.append(jugador)
        elif 'Medio' in jugador.posicion:
            medios.append(jugador)
        elif 'Delantero' in jugador.posicion:
            delanteros.append(jugador)

    result = {'porteros': porteros, 'defensas': defensas, 'medios': medios, 'delanteros': delanteros}

    return result


def ratingCalculte(jugadores, user, temporada):
    result = []
    searchValues = SearchValues.objects.get(user=user)
    for jugador in jugadores:
        rating = 0
        if temporada == '16/17' or temporada == '15/16':
            rendimiento = Performance.objects.all().filter(player=jugador, season=temporada)
        else:
            rendimiento = Performance.objects.all().filter(player=jugador)
        for r in rendimiento:

            rating = rating + r.squad * (searchValues.squad) if r.squad != None else rating + 0
            rating = rating + r.principal * (searchValues.principals) if r.principal != None else rating + 0
            rating = rating + r.yellowCards * (searchValues.yellowCards) if r.yellowCards != None else rating + 0
            rating = rating + r.redCards * (searchValues.redCards) if r.redCards != None else rating + 0

            if 'Portero' in jugador.position:

                rating = rating + r.goals * (searchValues.goalkeeper_goals) if r.goals != None else rating + 0
                rating = rating + r.assists * (searchValues.goalkeeper_assists) if r.assists != None else rating + 0
                rating = rating + r.ownGoals * (
                    searchValues.goalkeeper_ownGoals) if r.ownGoals != None else rating + 0

            elif 'Defensa' in jugador.position:

                rating = rating + r.goals * (searchValues.defence_goals) if r.goals != None else rating + 0
                rating = rating + r.assists * (searchValues.defence_assists) if r.assists != None else rating + 0
                rating = rating + r.ownGoals * (
                    searchValues.defence_ownGoals) if r.ownGoals != None else rating + 0

            elif 'Medio' in jugador.position:

                rating = rating + r.goals * (searchValues.midfield_goals) if r.goals != None else rating + 0
                rating = rating + r.assists * (searchValues.midfield_assists) if r.assists != None else rating + 0
                rating = rating + r.ownGoals * (
                    searchValues.midfield_ownGoals) if r.ownGoals != None else rating + 0

            elif 'Delantero' in jugador.position:

                rating = rating + r.goals * (searchValues.striker_goals) if r.goals != None else rating + 0
                rating = rating + r.assists * (searchValues.striker_assists) if r.assists != None else rating + 0
                rating = rating + r.ownGoals * (
                    searchValues.striker_ownGoals) if r.ownGoals != None else rating + 0

        jugador.rating = rating
        jugador.save()
        result.append(jugador)

    result = sorted(result, reverse=True)

    return result