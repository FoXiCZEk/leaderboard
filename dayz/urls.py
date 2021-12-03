from django.urls import path

from . import views

urlpatterns = [
    path('leaderboard', views.hello, name="leaderboard"),
    path('server_status', views.server_status, name="server_status"),
    path('', views.home, name="home"),
    path('tips_medical', views.tips_medical, name="tips_medical"),
    path('tips_craft', views.tips_craft, name="tips_craft")
]
