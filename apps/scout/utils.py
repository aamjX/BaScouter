from apps.scout.models import Performance, Like
from apps.usuario.models import SearchValues

'''----------------------------------------------------------------------------------------------------------'''

'''Funciones auxiliares'''

'''----------------------------------------------------------------------------------------------------------'''


def ordenarJugadores(players):
    porteros = []
    defensas = []
    medios = []
    delanteros = []

    for player in players:
        if 'Portero' in player.position:
            porteros.append(player)
        elif 'Defensa' in player.position:
            defensas.append(player)
        elif 'Medio' in player.position:
            medios.append(player)
        elif 'Delantero' in player.position:
            delanteros.append(player)

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


def favAlineaciones_ID_ByUser(principal_user):
    alinaciones_id = []
    user = principal_user
    user_meGustas = Like.objects.all().filter(user=user)

    for uMG in user_meGustas:
        alinaciones_id.append(uMG.squad.id)

    return alinaciones_id
