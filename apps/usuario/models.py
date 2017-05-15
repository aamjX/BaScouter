from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
import os
from datetime import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    sex = models.CharField(max_length=100, blank=False)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.URLField(max_length=500, blank=True)
    followed_by = models.ManyToManyField(User, related_name='followed_by')
    following = models.ManyToManyField(User, related_name='following')

    @classmethod
    def create(cls, user):
        profile = cls(user=user)
        return profile

class SearchValues(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    squad = models.FloatField(default=1,validators=[MaxValueValidator(10), MinValueValidator(-10)])
    principals = models.FloatField(default=2,validators=[MaxValueValidator(10), MinValueValidator(-10)])
    subtitutedOn = models.IntegerField(default=-1,validators=[MaxValueValidator(10), MinValueValidator(-10)])
    subtitutedOff = models.IntegerField(default=1,validators=[MaxValueValidator(10), MinValueValidator(-10)])
    yellowCards = models.FloatField(default=-1,validators=[MaxValueValidator(10), MinValueValidator(-10)])
    doubleYellowCards = models.IntegerField(default=-3, validators=[MaxValueValidator(10), MinValueValidator(-10)])
    redCards = models.FloatField(default=-6,validators=[MaxValueValidator(10), MinValueValidator(-10)])
    penaltyGoals = models.IntegerField(default=-1,validators=[MaxValueValidator(10), MinValueValidator(-10)])
    concededGoald = models.IntegerField(default=-1,validators=[MaxValueValidator(10), MinValueValidator(-10)])
    mathesWithoutGoals = models.IntegerField(default=3,validators=[MaxValueValidator(10), MinValueValidator(-10)])

    goalkeeper_goals = models.FloatField(default=6,validators=[MaxValueValidator(10), MinValueValidator(-10)])
    goalkeeper_assists = models.FloatField(default=5,validators=[MaxValueValidator(10), MinValueValidator(-10)])
    goalkeeper_ownGoals = models.FloatField(default=-6,validators=[MaxValueValidator(10), MinValueValidator(-10)])
    goalkeeper_minutesPorGoal = models.FloatField(default=-0.5,validators=[MaxValueValidator(10), MinValueValidator(-10)])

    defence_goals = models.FloatField(default=5,validators=[MaxValueValidator(10), MinValueValidator(-10)])
    defence_assists = models.FloatField(default=4,validators=[MaxValueValidator(10), MinValueValidator(-10)])
    defence_ownGoals = models.FloatField(default=-5,validators=[MaxValueValidator(10), MinValueValidator(-10)])
    defence_minutesPorGoal = models.FloatField(default=-1.5,validators=[MaxValueValidator(10), MinValueValidator(-10)])

    midfield_goals = models.FloatField(default=4.5,validators=[MaxValueValidator(10), MinValueValidator(-10)])
    midfield_assists = models.FloatField(default=3,validators=[MaxValueValidator(10), MinValueValidator(-10)])
    midfield_ownGoals = models.FloatField(default=-3.5,validators=[MaxValueValidator(10), MinValueValidator(-10)])
    midfield_minutesPorGoal = models.FloatField(default=-2,validators=[MaxValueValidator(10), MinValueValidator(-10)])

    striker_goals = models.FloatField(default=3,validators=[MaxValueValidator(10), MinValueValidator(-10)])
    striker_assists = models.FloatField(default=2,validators=[MaxValueValidator(10), MinValueValidator(-10)])
    striker_ownGoals = models.FloatField(default=-3,validators=[MaxValueValidator(10), MinValueValidator(-10)])
    striker_minutesPorGoal = models.FloatField(default=-3,validators=[MaxValueValidator(10), MinValueValidator(-10)])

    @classmethod
    def create(cls, user):
        searchValue = cls(user=user)
        return searchValue

class Comment(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='autor')
    text = models.TextField()
    created_date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.text