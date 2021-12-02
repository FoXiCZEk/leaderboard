from django.shortcuts import render
from .models import *
from .tables import *
import requests
import json
from django.http import HttpRequest, HttpResponse
# Create your views here.


def hello(request):
    if "sort" in request.GET.dict():
        sorting = request.GET.dict()['sort']
    else:
        sorting = '-name'
    players = Player.objects.order_by(sorting).reverse()
    table = PlayerTable(players)
    #deaths = Death.objects.order_by("steamId")
    #table_deaths = DeathTable(deaths)
    deaths = Test.objects.order_by('name')
    table_deaths = DeathPlayerTable(deaths)
    totalZCount = 0
    traveled = 0
    animal_kills = 0
    animalKiller = {}
    zombie_kills = 0
    zombieKiller = {}
    sniper_dist = 0
    sniper = {}
    for player in players:
        if player.animalsKilled > animal_kills:
            animal_kills = player.animalsKilled
            animalKiller['name'] = player.name
            animalKiller['count'] = player.animalsKilled
            animalKiller['steamid'] = player.steamId
        if player.zKilled > zombie_kills:
            zombie_kills = player.zKilled
            zombieKiller['name'] = player.name
            zombieKiller['count'] = player.zKilled
            zombieKiller['steamid'] = player.steamId
        if player.longestShot > sniper_dist:
            sniper_dist = player.longestShot
            sniper['name'] = player.name
            sniper['dist'] = player.longestShot
            sniper['steamid'] = player.steamId
        totalZCount += player.zKilled
        traveled += player.distTrav
    return render(request, 'dayz/test.html', {'players': table, 'deaths': table_deaths, 'zcount': totalZCount,
                                              'traveled': f"{traveled / 1000} km", 'animalKiller': animalKiller,
                                              'zombieKiller': zombieKiller, 'sniper': sniper})


def server_status(request):
    data = requests.get("https://query.fakaheda.eu/82.208.17.115:27582.feed")
    jdata = json.loads(data.text)
    memory = (int(jdata['memory']) / 1024) / 1024
    return render(request, 'dayz/server_status.html', {'data': jdata, "memory": memory})


