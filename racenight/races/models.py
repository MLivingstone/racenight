from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
from django.urls import reverse
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver

from .utils import distributeWinnings

class Race(models.Model):
    STATUS = (
        ('Upcoming', 'Upcoming'),
        ('In Play', 'In Play'),
        ('No More Bets', 'No More Bets'),
        ('Finished', 'Finished')
        )

    number = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    srcyoutube = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return self.name


class Horse(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class RaceEntry(models.Model):
    race = models.ForeignKey('Race', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=0)
    horse = models.OneToOneField('Horse', on_delete=models.CASCADE)
    won = models.BooleanField(default=False) 

    def __str__(self):
        return str(self.race) + ' ' + str(self.number) 


class Bet(models.Model):
    raceentry = models.ForeignKey('RaceEntry', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    winnings = models.PositiveIntegerField(default=0, blank=True)

    def get_absolute_url(self):
        # After update return to race dashboard
        return reverse('races:dashboard', kwargs={'pk': self.raceentry.race.id})
    
    def __str__(self):
        return str(self.raceentry)


@receiver(post_save, sender=Race)
def update_cash(sender, instance, **kwargs):
    print(f'SIGNAL: Race post_save on race {instance.id}')
    if instance.status == 'Finished':
        distributeWinnings(Bet, RaceEntry, instance.id)
   

# @receiver(post_save, sender=Bet)
# def update_bet(sender, instance, **kwargs):
#     print('SIGNAL: Bet post_save' )  
#     print(instance)
#     print(instance.amount)
 

# @receiver(pre_save, sender=Bet)
# def update_bet_pre_save(sender, instance, **kwargs):
#     print('SIGNAL: Bet pre-save')

