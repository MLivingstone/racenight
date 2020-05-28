from django.urls import path
from . import views

app_name = 'races'

urlpatterns = [
    path('dashboard/<int:pk>',views.dashboard, name='dashboard'),
    path('bet/create/<int:pk>', views.createBet, name="bet-create"),  
    path('bet/delete/<int:pk>/',views.deleteBet, name='bet-delete'),   
    path('leaderboard/',views.Leaderboard, name='leaderboard'),
    path('watchrace/<int:pk>/',views.WatchRace, name='watchrace'), 
    path('nextrace',views.WatchNextRace, name='watchnextrace'),       
]
