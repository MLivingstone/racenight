from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from races.models import *

@login_required
def maindashboard(request):
    raceentrys = RaceEntry.objects.all().order_by('number')
    bets = Bet.objects.filter(user=request.user)
    races = Race.objects.all()
    winners = RaceEntry.objects.filter(won=True)

    # context = {'raceentrys':raceentrys, 'bets':bets, 'race':race, 'race_status':status, 'winner':winner}

    context = {'bets':bets, 'races':races, 'winners':winners, 'raceentrys':raceentrys}

    return render(request, 'maindashboard.html', context)

@login_required
def home(request):
    raceentrys = RaceEntry.objects.all()
    bets = Bet.objects.filter(user=request.user)
    races = Race.objects.all()
    winners = RaceEntry.objects.filter(won=True)

    # context = {'raceentrys':raceentrys, 'bets':bets, 'race':race, 'race_status':status, 'winner':winner}

    context = {}

    return render(request, 'home.html', context)   

@login_required
def betHistory(request):

    races = Race.objects.all()
    bets = Bet.objects.filter(user=request.user)

    context = {'races':races, 'bets':bets}
    return render(request, 'bet_history.html', context) 


class HomePage(TemplateView):
    template_name = 'landing.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))
        return super().get(request, *args, **kwargs)