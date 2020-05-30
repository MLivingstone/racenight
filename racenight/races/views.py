from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from races.models import Bet, RaceEntry, Race
from races.forms import BetCreateForm, BetUpdateForm
from django.contrib.auth.decorators import login_required
from braces.views import SelectRelatedMixin
from django.http import Http404
from django.urls import reverse_lazy
from accounts.models import Profile
from django.views.decorators.cache import cache_control
from django.db.models import Sum
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()

@login_required
def dashboard(request, pk):
    raceentrys = RaceEntry.objects.filter(race=pk).order_by('number')
 
    bets = Bet.objects.filter(user=request.user, raceentry__race=pk)
    race = Race.objects.get(pk=pk)
    status = race.status

    betstotal = Bet.objects.filter(raceentry__race=pk)
    bets_total_amount = Bet.objects.filter(raceentry__race=pk).aggregate(Sum('amount'))['amount__sum']
    # Bets with winning horse
    bets_won = Bet.objects.filter(raceentry__race=pk, raceentry__won=True)
    bets_won_amount = Bet.objects.filter(raceentry__race=pk, raceentry__won=True).aggregate(Sum('amount'))['amount__sum']
    if bets_won:
        win_per_ticket = round(Decimal(bets_total_amount/bets_won_amount),1)
    else:
        win_per_ticket = 'No Winning Tickets!'

    if raceentrys:
        winner = RaceEntry.objects.get(race=pk, won=True)
    else:
        winner=""

    raceentry_bets = {}
    for raceentry in raceentrys:
        raceentry_bets[raceentry.id] = Bet.objects.filter(raceentry=raceentry).aggregate(Sum('amount'))['amount__sum']

    print(raceentry_bets)

    context = {'raceentrys':raceentrys, 'bets':bets, 'race':race, 'race_status':status, 'winner':winner,
                'bets_total_amount':bets_total_amount, 'raceentry_bets':raceentry_bets,
                'bets_winning':bets_won_amount, 'win_per_ticket':win_per_ticket}

    return render(request, 'races/dashboard.html', context)

@login_required
def createBet(request, pk):
    raceentry = RaceEntry.objects.get(id=pk)
    raceid = raceentry.race.id
    raceentrys = RaceEntry.objects.filter(race=raceid)
    race = Race.objects.get(id=raceid)
    bets = Bet.objects.filter(user=request.user, raceentry__race=raceid)
    user = request.user
    form = BetCreateForm(initial={'raceentry':raceentry, 'user':user, 'amount':1})
    status = race.status

    if request.method == 'POST':
        form = BetCreateForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.user = user
            form.raceentry = raceentry            
            cash = user.profile.cash
            user.profile.cash = cash - int(request.POST['amount'])
            try:
                request.user.save()
            except:
                messages.warning(request,'Insufficent funds. Please reduce the amount.')
            else:
                form.save()
                return redirect('maindashboard') 
        else:
            for error in form.errors:     
                messages.warning(request,form.errors.get(error)[0])
                
    context = {'form':form, 'betslip':raceentry, 'raceentrys':raceentrys, 'bets':bets, 'race':race, 'race_status':status}
    return render(request, 'races/dashboard.html', context) 


def deleteBet(request, pk):
    bet = Bet.objects.get(id=pk)
    raceid = bet.raceentry.race.id
    request.user.profile.cash = request.user.profile.cash + bet.amount
    request.user.save()
    bet.delete()
    return redirect('races:dashboard', raceid)
 

# class BetCreateView(LoginRequiredMixin, CreateView):
#     model = Bet
#     fields = ('raceentry', 'amount')

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.user = self.request.user
#         self.object.save()
#         return super().form_valid(form)  

@login_required
def Leaderboard(request):
    profiles = Profile.objects.all().order_by('-cash')

    context = {'profiles':profiles}

    return render(request, 'races/leaderboard.html', context)

@login_required
def WatchRace(request, pk):
    race = Race.objects.get(pk=pk)

    context = {'race':race}

    return render(request, 'races/watchrace.html', context)

@login_required
def WatchNextRace(request):
    races = ['In Play', 'No More Bets']
    nextrace = Race.objects.filter(status__in = races).first()

    context = {'race':nextrace}

    return render(request, 'races/watchrace.html', context)