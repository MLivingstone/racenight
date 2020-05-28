from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models import F

def distributeWinnings(Bet, RaceEntry, raceid):
    
    print('DISTRIBUTE WINNINGS')
    # All bets placed on this race
    # bets_all = Bet.objects.filter(raceentry__race=raceid)
    bets_all_amount = Bet.objects.filter(raceentry__race=raceid).aggregate(Sum('amount'))['amount__sum']

    # Bets with winning horse
    bets_won = Bet.objects.filter(raceentry__race=raceid, raceentry__won=True)
    bets_won_amount = Bet.objects.filter(raceentry__race=raceid, raceentry__won=True).aggregate(Sum('amount'))['amount__sum']

    if bets_won:
        win_per_ticket = bets_all_amount/bets_won_amount

        # print('bet_tickets {} winning_tickets {}'.format(bets_all_amount,bets_won_amount))
        # print(f'win per ticket {win_per_ticket}')

        for bet in bets_won:
            user = bet.user
            winnings = bet.amount * win_per_ticket
            bet.winnings = winnings
            bet.save()
            # user.profile.update(cash = F('cash') + winnings)
            user.profile.cash = user.profile.cash + winnings
            user.save()
    else:
        print('No winning bets!')



