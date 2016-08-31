from django.contrib import admin

from ranking.models import Player, Team, Match

class PlayerAdmin(admin.ModelAdmin):
    list_display = ("__unicode__", "mu", "sigma")
    ordering = ["-mu"]

admin.site.register(Player, PlayerAdmin)

class MatchAdmin(admin.ModelAdmin):
    list_display = ("__unicode__", "time")
    ordering = ["time"]

admin.site.register(Match, MatchAdmin)

class TeamAdmin(admin.ModelAdmin):
    list_display = ("__unicode__", "mu", "sigma")
    ordering = ["-mu"]

admin.site.register(Team, TeamAdmin)
