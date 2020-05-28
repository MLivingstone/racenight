import os
# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE','racenight.settings')

import django
# Import settings
django.setup()

from races.models import *

import pandas as pd

def populate_races():
    # Upload races
    print('Races uploading...')
    races = pd.read_csv('Races.csv')
    for index, race in races.iterrows():
        x = Race.objects.get_or_create(
            number = race['number'],
            name = race['name'],
            status = race['status']
        )
    print('Races upload complete')


def populate_horses():
    # Upload horses
    print('Horses uploading...')
    horses = pd.read_csv('horses.csv')
    for index, horse in horses.iterrows():
        x = Horse.objects.get_or_create(
            name = horse['name']
        )
    print('Horses upload complete')    


def populate_raceentrys():
    # Upload raceentry
    print('Raceentrys uploading...')
    raceentrys = pd.read_csv('raceentrys.csv')
    for index, raceentry in raceentrys.iterrows():
        x = RaceEntry.objects.get_or_create(
            race = Race.objects.get(number=raceentry['race']),
            number = raceentry['number'],
            horse = Horse.objects.get(name=raceentry['horse']),
            won = raceentry['won']
        )
    print('Raceentrys upload complete')    


if __name__ == '__main__':
    print("Populating the databases...Please Wait")
    populate_races()
    populate_horses()
    populate_raceentrys()
    print('Populating Complete')
