from __future__ import unicode_literals

from django.db import models

from trueskill import Rating, rate, rate_1vs1

class Rated(models.Model):
    mu = models.FloatField(blank=False, null=False, default=25)
    sigma = models.FloatField(blank=False, null=False, default=8.333)

    class Meta:
        abstract = True

class Player(Rated):
    name = models.CharField(max_length=60, blank=False, null=False)

    def __unicode__(self):
        return u"%s" % self.name
    
class Team(Rated):
    players = models.ManyToManyField(Player)

    def __unicode__(self):
        return u" & ".join([p.name for p in self.players.all().order_by('name')])
    
class Match(models.Model):
    time = models.DateField(auto_now_add=True)
    winner = models.ForeignKey(Team, blank=False, null=False, related_name="winner")
    loser = models.ForeignKey(Team, blank=False, null=False, related_name="loser")

    def save(self, *args, **kwargs):
        winner_rating = Rating(mu=self.winner.mu, sigma=self.winner.sigma)
        loser_rating = Rating(mu=self.loser.mu, sigma=self.loser.sigma)

        new_winner_rating, new_loser_rating = rate_1vs1(winner_rating, loser_rating)

        self.winner.mu = new_winner_rating.mu
        self.winner.sigma = new_winner_rating.sigma
        self.winner.save()

        self.loser.mu = new_loser_rating.mu
        self.loser.sigma = new_loser_rating.sigma
        self.loser.save()

        # Personal rating
        winners = {p: Rating(mu=p.mu, sigma=p.sigma) for p in self.winner.players.all()}
        losers = {p: Rating(mu=p.mu, sigma=p.sigma) for p in self.loser.players.all()}        
        # Score the match
        new_team_ratings = rate([winners, losers]) # Returns a list with a one or many dicts

        for team in new_team_ratings:
            for player, new_rating in team.iteritems():
                player.mu = new_rating.mu
                player.sigma = new_rating.sigma
                player.save()

        super(Match, self).save(*args, **kwargs)


    def __unicode__(self):
        return u"%s vs %s" % (self.winner, self.loser)
