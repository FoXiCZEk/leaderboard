from django.db import models

# Create your models here.


class Player(models.Model):
    steamId = models.CharField(max_length=18)
    deaths = models.IntegerField()
    kills = models.IntegerField()
    animalsKilled = models.IntegerField()
    name = models.CharField(max_length=250)
    lastTimeSeen = models.DateTimeField()
    deathsToZCount = models.IntegerField()
    deathsToNaturalCauseCount = models.IntegerField()
    deathsToPlayerCount = models.IntegerField()
    deathsToAnimalCount = models.IntegerField()
    suicideCount = models.IntegerField()
    longestShot = models.FloatField()
    zKilled = models.IntegerField()
    timeSurvived = models.IntegerField()
    distTrav = models.IntegerField()

    class Meta:
        db_table = "dayz_players"
        managed = False

    def __str__(self):
        return f"steamId={self.steamId}, name={self.name}"


class Death(models.Model):
    steamId = models.CharField(max_length=18)
    animalsKilled = models.IntegerField()
    kills = models.IntegerField()
    longestShot = models.IntegerField()
    timeSurvived = models.IntegerField()
    zKillCount = models.IntegerField()
    distTrav = models.IntegerField()
    timeStamp = models.IntegerField()
    posDeath = models.CharField(max_length=150)
    killer = models.CharField(max_length=100)
    weapon = models.CharField(max_length=100)

    class Meta:
        db_table = "dayz_death"
        managed = False


class Test(models.Model):
    name = models.CharField(max_length=250)
    animalsKilled = models.IntegerField()
    kills = models.IntegerField()
    longestShot = models.IntegerField()
    timeSurvived = models.IntegerField()
    zKillCount = models.IntegerField()
    distTrav = models.IntegerField()
    killer = models.CharField(max_length=100)
    weapon = models.CharField(max_length=100)

    class Meta:
        db_table = 'dayz_death_player'
        managed = False


