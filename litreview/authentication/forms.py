# authentication/forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    """
    Form that get the new account information from the user
    """
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username",)
        help_texts = {"username": None}
