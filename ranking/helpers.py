from ranking.models import Player, Team, Match
from trueskill import Rating, rate, rate_1vs1

def RatingRecount():
    player_ratings = {p: Rating() for p in Player.objects.all()}
    team_ratings = {t: Rating() for t in Team.objects.all()}

    print "#"*60
    print "RECOUNTING #"*4
    print "#"*60
    
    for match in Match.objects.order_by("id"):
        # Get ratings for players
        winners = {p: player_ratings[p] for p in match.winner.players.all()}
        losers = {p: player_ratings[p] for p in match.loser.players.all()}
        
        # Score the match
        new_team_ratings = rate([winners, losers]) # Returns a list with a one or many dicts

        for team in new_team_ratings:
            for player, new_rating in team.iteritems():
                player_ratings[player] = new_rating # save to database

        # Team ranking
        team_ratings[match.winner], team_ratings[match.loser] = rate_1vs1(team_ratings[match.winner], team_ratings[match.loser])
        
    for player, rating in player_ratings.iteritems():
        print player, " - ", rating.mu
        player.mu = rating.mu
        player.sigma = rating.sigma
        player.save()

    for team, rating in team_ratings.iteritems():
        print team, " - ", rating.mu, team.mu
        

    

