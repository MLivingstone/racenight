from django.contrib import admin
from races.models import Race, Horse, RaceEntry, Bet

admin.site.register(Horse)

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'status', 'srcyoutube',)
    list_editable = ('srcyoutube','status',)

@admin.register(RaceEntry)
class RaceEntryAdmin(admin.ModelAdmin):
    list_display = ('race', 'number', 'horse', 'won')
    list_filter = ('race',)
    list_editable = ('won',)

@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ('raceentry', 'amount', 'user')