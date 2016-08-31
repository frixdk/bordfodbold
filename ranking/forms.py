from django import forms
from ranking.models import Player, Team, Match

class NewMatchForm(forms.Form):

    winner_1 = forms.ModelChoiceField(queryset=Player.objects.all(), empty_label="", required=True)
    winner_2 = forms.ModelChoiceField(queryset=Player.objects.all(), empty_label="", required=True)
    loser_1 = forms.ModelChoiceField(queryset=Player.objects.all(), empty_label="", required=True)
    loser_2 = forms.ModelChoiceField(queryset=Player.objects.all(), empty_label="", required=True)

    def __init__(self, *args, **kwargs):
        super(NewMatchForm, self).__init__(*args, **kwargs)
        bootstrap_class = "form-control"
        self.fields['winner_1'].widget.attrs['class'] = bootstrap_class
        self.fields['winner_2'].widget.attrs['class'] = bootstrap_class
        self.fields['loser_1'].widget.attrs['class'] = bootstrap_class
        self.fields['loser_2'].widget.attrs['class'] = bootstrap_class
        
    def clean(self):
        data = self.cleaned_data
        players = []

        for field_name in self.fields:
            players.append(data.get(field_name, None))

        if len(set(players)) != 4 or None in players:
            self._errors["integrity"] = ["You suck at forms"]
            
        return data
