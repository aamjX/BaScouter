import csv
from datetime import datetime
import MySQLdb
from django.core.management.base import BaseCommand
from apps.scout.models import Championship


class Command(BaseCommand):
    help = 'Este comando se utiliza para popular la BBDD'

    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASS = 'p@ssW0rd'
    DB_NAME = 'bascouter'

    def _create_championship(self):
        cont = 0
        with open('apps/scout/management/data/Competiciones.csv', 'rt', encoding='utf8') as csvfile:
            competicionesReader = csv.reader(csvfile, delimiter=',')
            for row in competicionesReader:
                if cont == 0:
                    cont += 1
                else:
                    logo = 'http://'+row[2][2:]
                    c = Championship(name=row[1], logo=logo, category=row[3])
                    c.save()

    def _create_teams(self):

        datos = [self.DB_HOST, self.DB_USER, self.DB_PASS, self.DB_NAME]

        conn = MySQLdb.connect(*datos)
        conn.set_character_set('utf8mb4')
        cursor = conn.cursor()
        cursor.execute("SET NAMES utf8mb4;")
        cursor.execute("SET CHARACTER SET utf8mb4;")
        cursor.execute("SET character_set_connection=utf8mb4;")
        cont = 0
        with open('apps/scout/management/data/Equipos.csv', 'rt', encoding='utf8') as csvfile:
            equiposReader = csv.reader(csvfile, delimiter=',')
            for row in equiposReader:
                if cont == 0:
                    cont += 1
                else:
                    escudo = 'http://'+row[3][2:]
                    cursor.execute('''INSERT INTO scout_team (championship_id, name ,badge, squad, avgAge, foreignCount, value) VALUES (%s,%s,%s,%s,%s,%s,%s)''',
                                   (round(float(row[1])) + 1, row[2], escudo, row[4], self.convertAltura(row[5]), row[6], self.convertValue(row[7])))

        conn.commit()
        cursor.close()
        conn.close()

    def _create_players(self):

        datos = [self.DB_HOST, self.DB_USER, self.DB_PASS, self.DB_NAME]

        conn = MySQLdb.connect(*datos)
        conn.set_character_set('utf8mb4')
        cursor = conn.cursor()
        cursor.execute("SET NAMES utf8mb4")
        cursor.execute("SET CHARACTER SET utf8mb4;")
        cursor.execute("SET character_set_connection=utf8mb4;")
        cont = 0
        with open('apps/scout/management/data/Jugadores.csv', 'rt', encoding='utf8') as csvfile:
            jugadoresReader = csv.reader(csvfile, delimiter=',')
            for r in jugadoresReader:
                if cont == 0:
                    cont += 1
                else:

                    row = self.formatRowForPlayers(r)
                    avatar = 'http://' + row[1]
                    bandera ='http://'+row[6][2:]

                    cursor.execute('''INSERT INTO scout_player (team_id, image, name, fullName, number,
                                  nationality, flag, birthDate, age, birthPlace, value, position, height, foot,
                                  contractUntil, inTheTeamSince, agent, outfitter) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                                   (round(float(row[8])) + 1, avatar, row[2], row[3], row[4], row[5],
                                    bandera, self.stringToDate(row[12]),row[11], row[17], self.convertValue(row[7]), row[14],
                                    self.convertAltura(row[9]), row[10],
                                    self.stringToDate(row[13]), self.stringToDate(row[15]), row[16], row[18]))

        conn.commit()
        cursor.close()
        conn.close()

    def _create_performance(self):

        datos = [self.DB_HOST, self.DB_USER, self.DB_PASS, self.DB_NAME]

        conn = MySQLdb.connect(*datos)
        conn.set_character_set('utf8mb4')
        cursor = conn.cursor()
        cursor.execute("SET NAMES utf8mb4;")
        cursor.execute("SET CHARACTER SET utf8mb4;")
        cursor.execute("SET character_set_connection=utf8mb4;")
        cont = 0
        with open('apps/scout/management/data/Rendimiento_jugadores.csv', 'rt', encoding='utf8') as csvfile:
            rendimientoReader = csv.reader(csvfile, delimiter=',')
            for row in rendimientoReader:
                if cont == 0:
                    cont += 1
                else:
                    row = self.formatRowForPerformance(row)
                    cursor.execute('''INSERT INTO scout_performance (player_id, season, championship, club, squad,
                                    principal, pointsPerMatch, goals, assists, ownGoals, subtitutedOn, subtitutedOff, yellowCards,
                                    doubleYellowCards, redCards, penaltyGoals, minutesPorGoal, minutesPlayed, concededGoald, mathesWithoutGoals) VALUES (%s,%s,%s,%s,%s,
                                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                                   (round(float(row[1])) + 1, row[2], row[3], row[4], row[5],
                                    row[6], self.convertPuntosPorPartido(row[7]), row[8], row[9], row[10], row[11],
                                    row[12], row[13], row[14],
                                    row[15], row[16], self.converMinutosJugados(row[17]),
                                    self.converMinutosJugados(row[18]), row[19], row[20]))

            conn.commit()
            cursor.close()
            conn.close()

    def _create_history(self):

        datos = [self.DB_HOST, self.DB_USER, self.DB_PASS, self.DB_NAME]

        conn = MySQLdb.connect(*datos)
        conn.set_character_set('utf8mb4')
        cursor = conn.cursor()
        cursor.execute("SET NAMES utf8mb4;")
        cursor.execute("SET CHARACTER SET utf8mb4;")
        cursor.execute("SET character_set_connection=utf8mb4;")
        cont = 0

        with open('apps/scout/management/data/Historial_fichajes_jugadores.csv', 'rt', encoding='utf8') as csvfile:
            historialReader = csv.reader(csvfile, delimiter=',')
            for row in historialReader:
                if cont == 0:
                    cont += 1
                else:

                    cursor.execute(
                        '''INSERT INTO scout_history(player_id, season, date, movingFrom, movingTo, value, cost) VALUES (%s,%s,%s,%s,%s,%s,%s)''',
                        (round(float(row[1])) + 1, row[2], self.stringToDate(row[3]),row[4], row[5],
                         self.convertValue(row[6]), row[7].split('.')[0]))

        conn.commit()
        cursor.close()
        conn.close()

    def run_query(self, query=''):

        datos = [self.DB_HOST, self.DB_USER, self.DB_PASS, self.DB_NAME]

        conn = MySQLdb.connect(*datos)
        cursor = conn.cursor()
        cursor.execute(query)

        if query.upper().startswith('SELECT'):
            data = cursor.fetchall()
        else:
            conn.commit()
            data = None

        cursor.close()
        conn.close()

        return data

    def run_sql_script(self, path=''):

        datos = [self.DB_HOST, self.DB_USER, self.DB_PASS, self.DB_NAME]

        conn = MySQLdb.connect(*datos)
        cursor = conn.cursor()

        for query in open(path):
            cursor.execute(query)

        cursor.close()
        conn.close()

    def truncate_tables(self):
        self.run_sql_script('apps/scout/management/scripts/truncate_tables.sql')

    def stringToDate(self, string):
        try:
            if string != None:
                string = string.split(' ')
                result = datetime.strptime(str(string[0]).replace('.', '/'), '%d/%m/%Y')
            else:
                result = None
        except ValueError:
            result = None
        return result

    def convertValue(self, value):
        try:
            if 'miles' in value:
                v = value.split(' ')
                result = float(v[0].replace(',', '.')) * 1000
            elif 'Fin' in value or 'Tarifa' in value:
                return None
            else:
                v = value.split(' ')
                if len(v) != 3:
                    result = None
                else:
                    result = float(v[0].replace(',', '.')) * 1000000
        except AttributeError:
            result = None

        return result

    def convertAltura(self, altura):
        try:
            a = altura.replace(',', '.')
            result = float(a.replace('m', ''))
        except AttributeError:
            result = None

        return result

    def formatRowForPlayers(self, row):
        for i in range(len(row)):
            if row[i] == '-' and i != 4 and i != 9:
                row[i] = ''
            elif row[i] == '-' and (i == 4 or i == 9):
                row[i] = None
            else:
                next
        return row

    def formatRowForPerformance(self, row):
        for i in range(len(row)):
            if row[i] == '-':
                row[i] = None
            else:
                next
        return row

    def converMinutosJugados(self, string):
        if string == None:
            return None
        else:
            return string.replace('.', '').replace('\'', '')

    def convertPuntosPorPartido(self, string):
        if string == None:
            return None
        else:
            return string.replace(',', '.')

    def handle(self, *args, **options):
        self.truncate_tables()
        self._create_championship()
        self._create_teams()
        self._create_players()
        self._create_performance()
        self._create_history()