from django.db import models
from django.core.validators import URLValidator
from functools import total_ordering
from django.contrib.auth.models import User

class Championship(models.Model):
    name = models.CharField(max_length=100)
    logo = models.URLField(validators=[URLValidator()])
    category = models.CharField(max_length=100)


class Team(models.Model):
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    badge = models.URLField(validators=[URLValidator()], null=True)
    squad = models.IntegerField(null=True)
    avgAge = models.IntegerField(null=True)
    foreignCount = models.IntegerField(null=True)
    value = models.FloatField(null=True)

@total_ordering
class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    image = models.URLField(validators=[URLValidator()], null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    fullName = models.CharField(max_length=100, blank=True, null=True)
    number = models.IntegerField(null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    flag = models.URLField(validators=[URLValidator()], null=True)
    birthDate = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True)
    birthPlace = models.CharField(max_length=150, blank=True, null=True)
    value = models.FloatField(null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    height = models.FloatField(null=True)
    foot = models.CharField(max_length=50, blank=True, null=True)
    contractUntil = models.DateField(null=True)
    inTheTeamSince = models.DateField(null=True)
    agent = models.CharField(max_length=150, blank=True, null=True)
    outfitter = models.CharField(max_length=100, null=True)
    rating = models.FloatField(null=True)
    likes = models.IntegerField(null=True, default=0)

    def __lt__(self, other):
        return (self.rating < other.rating)

    def __eq__(self, other):
        return self.rating == other.rating

class History(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.CharField(max_length=10, null=True)
    date = models.DateField(null=True)
    movingFrom = models.CharField(max_length=100, null=True)
    movingTo = models.CharField(max_length=100, null=True)
    value = models.FloatField(null=True)
    cost = models.CharField(max_length=150, null=True)


class Performance(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.CharField(max_length=20)
    championship = models.CharField(max_length=150)
    club = models.CharField(max_length=150, blank=True)
    squad = models.IntegerField(null=True)
    principal = models.IntegerField(null=True)
    pointsPerMatch = models.FloatField(null=True)
    goals = models.IntegerField(null=True)
    assists = models.IntegerField(null=True)
    ownGoals = models.IntegerField(null=True)
    subtitutedOn = models.IntegerField(null=True)
    subtitutedOff = models.IntegerField(null=True)
    yellowCards = models.IntegerField(null=True)
    doubleYellowCards = models.IntegerField(null=True)
    redCards = models.IntegerField(null=True)
    penaltyGoals = models.IntegerField(null=True)
    minutesPorGoal = models.FloatField(null=True)
    minutesPlayed = models.IntegerField(null=True)
    concededGoald = models.IntegerField(null=True)
    mathesWithoutGoals = models.IntegerField(null=True)

class Squad(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, default="Sin título")
    players = models.ManyToManyField(Player, related_name='players')
    principals = models.ManyToManyField(Player, related_name='principals')
    value = models.FloatField(default=0.0)
    averageAge = models.IntegerField(default=0)
    likeCount = models.IntegerField(default=0)
    description = models.TextField(default="Sin descripción")
    lastUpdate = models.DateField(null=True, blank=True)

    @classmethod
    def create(cls, user):
        squad = cls(user=user)
        return squad


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    squad = models.ForeignKey(Squad, on_delete=models.CASCADE)

    @classmethod
    def create(cls, user, squad):
        like = cls(user=user, squad=squad)
        return like

