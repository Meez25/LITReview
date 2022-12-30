from django import forms
from authentication.models import User

from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ("title", "description", "image")
        labels = {"title": "Titre"}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ["headline", "rating", "body"]
        labels = {"headline": "Titre", "rating": "Note", "body": "Commentaire"}
        widgets = {
            "rating": forms.widgets.RadioSelect(
                choices=[(i, " - " + str(i)) for i in range(6)]
            ),
        }


class FollowForm(forms.Form):
    followed_user = forms.CharField(
        label="Utilisateur à suivre",
        required=True,
    )
    follow_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class UnfollowForm(forms.Form):
    user_to_unfollow = forms.CharField(widget=forms.HiddenInput, required=False)
