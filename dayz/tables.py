import django_tables2 as tables
from django.utils.html import format_html
import datetime
from .models import Player, Death, Test


class PlayerTable(tables.Table):
    name = tables.Column(attrs={'td': {'font-weight': 'bold'}})
    lastTimeSeen = tables.DateTimeColumn(format='d.n.Y H:i:s')
    timeSurvived = tables.Column(attrs={'td': {'text-align': 'center'}})
    distTrav = tables.Column(attrs={'td': {'text-align': 'center'}})

    def render_name(self, value):
        return format_html(f"<b>{value}</b>")

    def render_timeSurvived(self, value):
        return str(datetime.timedelta(seconds=value))

    def render_distTrav(self, value):
        km = value / 1000
        return str(f"{km} km")

    class Meta:
        model = Player
        attrs = {"class": "table .table-hover", "id": "table_player"}
        template_name = "django_tables2/bootstrap.html"
        sequence = ('name', 'deaths', 'kills', 'animalsKilled', 'lastTimeSeen',
                    'deathsToZCount', 'deathsToNaturalCauseCount', 'deathsToPlayerCount',
                    'deathsToAnimalCount', 'suicideCount', 'longestShot', 'zKilled',
                    'timeSurvived', 'distTrav')
        fields = ['name', 'deaths', 'kills', 'animalsKilled', 'lastTimeSeen',
                  'deathsToZCount', 'deathsToNaturalCauseCount', 'deathsToPlayerCount',
                  'deathsToAnimalCount', 'suicideCount', 'longestShot', 'zKilled',
                  'timeSurvived', 'distTrav']
        exclude = ('steamId', )


class DeathTable(tables.Table):

    class Meta:
        model = Death
        template_name = "django_tables2/bootstrap.html"
        sequence = ('steamId', 'animalsKilled', 'kills', 'longestShot',
                    'timeSurvived', 'zKillCount', 'distTrav', 'timeStamp', 'killer', 'weapon')
        fields = ['steamId', 'animalsKilled', 'kills', 'longestShot',
                  'timeSurvived', 'zKillCount', 'distTrav', 'timeStamp', 'killer', 'weapon']
        exclude = ('steamId',)


class DeathPlayerTable(tables.Table):
    timeSurvived = tables.TimeColumn(format='H:i:s')

    def render_name(self, value):
        return format_html(f"<b>{value}</b>")

    def render_distTrav(self, value):
        km = value / 1000
        return str(f"{km} km")

    class Meta:
        model = Test
        orderable = False
        attrs = {"class": "table .table-hover", "id": "table_death"}
        sequence = ('name', 'animalsKilled', 'kills', 'longestShot',
                    'timeSurvived', 'zKillCount', 'distTrav', 'killer', 'weapon')
        fields = ['name', 'animalsKilled', 'kills', 'longestShot',
                  'timeSurvived', 'zKillCount', 'distTrav', 'killer', 'weapon']


