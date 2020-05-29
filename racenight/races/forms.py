from django import forms
from django.forms import ModelForm
from django.contrib import messages
from django.core import validators

from races.models import Bet

class BetCreateForm(ModelForm):
    # amount = forms.IntegerField(label='',widget=forms.TextInput(attrs={'placeholder':'Stake amount'}))

    class Meta:
        model = Bet
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(),
            'raceentry': forms.HiddenInput(),
        }
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not (amount>0):
            raise forms.ValidationError('Stake must be greater than zero',
                                        code='InvalidAmount')
        return amount

    def clean(self):
        # Check that a bet has not already been placed on this entry
        # overriding the clean method because we need access to the to the other fields, namely user 
        raceentry = self.cleaned_data['raceentry']
        user = self.cleaned_data.get('user')
        bets = Bet.objects.filter(user=user)
        for bet in bets:
            if raceentry == bet.raceentry:
                raise forms.ValidationError('You have already bet on this horse',
                                            code='InvalidSelection')

        # This error only happens if user had opened the create bet form and tries to place a bet if the race is no longer in-play
        if (raceentry.race.status != 'In Play'):
            raise forms.ValidationError('Sorry - no more bets!',
                                        code='InvalidSelection')
        return self.cleaned_data

class BetUpdateForm(ModelForm):
    class Meta:
        model = Bet
        fields = ['user','raceentry','amount']
        widgets = {
            'user': forms.HiddenInput(),
            'raceentry': forms.HiddenInput(),
        }
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not (amount>0):
            raise forms.ValidationError('Stake must be greater than zero',
                                        code='InvalidAmount')
        return amount

