from django import forms

from . import models


class TicketForm(forms.ModelForm):
    """
    Form to update of create a ticket
    """
    class Meta:
        model = models.Ticket
        fields = ("title", "description", "image")
        labels = {"title": "Titre"}


class ReviewForm(forms.ModelForm):
    """
    Form to update or create a review
    """
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
    """
    Form to allow one user to follow a second user
    """
    followed_user = forms.CharField(
        label="Utilisateur à suivre",
        required=True,
    )
    follow_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class UnfollowForm(forms.Form):
    """
    Form to remove the follow relation between two users
    """
    user_to_unfollow = forms.CharField(widget=forms.HiddenInput,
                                       required=False)
