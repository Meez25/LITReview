from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from critics.models import Ticket, Review, UserFollows
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TicketForm, ReviewForm, FollowForm
from authentication.models import User
from django.db import IntegrityError

# Create your views here.


@login_required
def flux(request):
    all_tickets = Ticket.objects.all()
    context = {
        "tickets": all_tickets,
    }
    return render(request, "critics/base_flux.html", context)


@login_required
def my_posts(request):
    user = request.user
    all_tickets = Ticket.objects.filter(user__exact=user).order_by("-time_created")
    context = {
        "tickets": all_tickets,
    }
    return render(request, "critics/my_posts.html", context)


@login_required
def abonnement(request):
    if request.method == "POST":
        form = FollowForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["followed_user"]
            current_user = request.user
            try:
                user_follow = User.objects.get(username__exact=username)
                if user_follow == current_user:
                    form = FollowForm()
                    context = {
                        "userfollow_form": form,
                        "error": "Vous ne pouvez pas vous suivre vous-même.",
                    }
                    return render(request, "critics/abonnement.html", context)

                if user_follow:
                    UserFollows.objects.create(
                        user=current_user, followed_user=user_follow
                    )
            except User.DoesNotExist:
                form = FollowForm()
                context = {
                    "userfollow_form": form,
                    "error": "L'utilisateur n'existe pas.",
                }
                return render(request, "critics/abonnement.html", context)
            except IntegrityError:
                form = FollowForm()
                context = {
                    "userfollow_form": form,
                    "error": "L'utilisateur est déjà suivi.",
                }
                return render(request, "critics/abonnement.html", context)

    else:
        form = FollowForm()
    context = {
        "userfollow_form": form,
    }

    return render(request, "critics/abonnement.html", context)


@login_required
def modify_post(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket_form = TicketForm(instance=ticket)
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, instance=ticket)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user  # Add the user to the ticket object
            ticket.save()
            return redirect("flux")
    context = {
        "ticket": ticket,
        "ticket_form": ticket_form,
    }
    return render(request, "critics/modify_post.html", context)


class TicketCreateView(LoginRequiredMixin, CreateView):
    form = TicketForm()
    model = Ticket
    fields = ["title", "description", "image"]
    success_url = "/flux/"

    """def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)"""

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


@login_required
def create_review(request):
    # Create two forms for the review form
    ticket_form = TicketForm()
    review_form = ReviewForm()
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user  # Add the user to the ticket object
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket  # Add the ticket to the review object
            review.user = request.user  # Add the user to the review object
            review.save()
            return redirect("flux")
    context = {
        "ticket_form": ticket_form,
        "review_form": review_form,
    }
    return render(request, "critics/review_form.html", context=context)
