# authentication/views.py
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render

from . import forms


def signup_page(request):
    """
    Function to display the signup page
    """
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, "authentication/signup.html",
                  context={"form": form})
