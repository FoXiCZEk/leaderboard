from django.urls import path

from . import views

urlpatterns = [
    path('leaderboard', views.hello, name="leaderboard"),
    path('server_status', views.server_status, name="server_status")
]
