from races.models import Race

# def races(request):
#     r1 = Race.objects.get(number=1).id
#     r2 = Race.objects.get(number=2).id
#     return {
#         'r1': r1, 'r2': r2, 
#     }

def get_race_numbers(request):
    race_ID = []
    races = Race.objects.all().order_by('number')
    for race in races:
        race_ID.append(race.id)

    if races:
        context = { 'race_one':     race_ID[0], 
                    'race_two':     race_ID[1], 
                    'race_three':   race_ID[2],
                    'race_four':    race_ID[3],
                    'race_five':    race_ID[4],}
    else:
       context = { 'race_one':     1, 
                    'race_two':     2, 
                    'race_three':   3,
                    'race_four':    4,
                    'race_five':    5,}

    return context

def get_race_status(request):
    race_status = []
    races = Race.objects.all().order_by('number')
    for race in races:
        race_status.append(race.status) 

    if races:
        context = { 'race_status_one':     race_status[0], 
                    'race_status_two':     race_status[1], 
                    'race_status_three':   race_status[2],
                    'race_status_four':    race_status[3],
                    'race_status_five':    race_status[4],
    }
    else:
        context = { 'race_status_one':     'Upcoming', 
                    'race_status_two':     'Upcoming', 
                    'race_status_three':   'Upcoming', 
                    'race_status_four':    'Upcoming', 
                    'race_status_five':    'Upcoming',
    }
    return context