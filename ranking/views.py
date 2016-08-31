from django.shortcuts import render
from ranking.models import Player, Team, Match
from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.db.models import Count
from forms import NewMatchForm
from ranking.helpers import RatingRecount

def overview(request):

    # New personal rating fucker test
    #RatingRecount() # recounts all ratings
    
    add_match_form = NewMatchForm()

    #print "wut SESSION", request.session
    
    if request.method == "POST":
        form = NewMatchForm(request.POST)

        if form.is_valid():
            winner_1 = form.cleaned_data["winner_1"]
            winner_2 = form.cleaned_data["winner_2"]
            loser_1 = form.cleaned_data["loser_1"]
            loser_2 = form.cleaned_data["loser_2"]
            winner_team = Team.objects.filter(players=winner_1).filter(players=winner_2).first()
            loser_team = Team.objects.filter(players=loser_1).filter(players=loser_2).first()

            if not winner_team:
                winner_team = Team()
                winner_team.save()
                winner_team.players.add(winner_1, winner_2)
            if not loser_team:
                loser_team = Team()
                loser_team.save()
                loser_team.players.add(loser_1, loser_2)

            match = Match.objects.create(winner=winner_team, loser=loser_team)
            
            return redirect('overview')
        else:
            add_match_form = form

    teams = Team.objects.annotate(player_count=Count("players")).filter(player_count__gt=1).order_by("-mu")

    for team in teams:
        team.player_list = team.players.all().order_by('name')
        team.won = Match.objects.filter(winner=team).count()
        team.lost = Match.objects.filter(loser=team).count()
        team.played = team.won + team.lost
        team.win_ratio = round(float(team.won)/team.lost, 2) if team.lost else 9000

    players = Player.objects.order_by("-mu")
    for player in players:
        player.won = Match.objects.filter(winner__players=player).count()
        player.lost = Match.objects.filter(loser__players=player).count()
        player.played = player.won + player.lost
        player.win_ratio = round(float(player.won)/player.lost, 2) if player.lost else 9000


    matches = Match.objects.count()
    
    context = {
        "teams": teams,
        "players": players,
        "matches": matches,
        "form": add_match_form,
    }
    
    return render(request, 'ranking/index.html', context)    
