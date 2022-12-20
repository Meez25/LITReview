from django import forms
from authentication.models import User

from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ["rating", "headline", "body"]


class FollowForm(forms.Form):
    followed_user = forms.CharField(
        label="Utilisateur à suivre",
        required=True,
    )
