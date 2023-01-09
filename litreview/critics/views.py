from itertools import chain

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from critics.models import Ticket, Review, UserFollows
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TicketForm, ReviewForm, FollowForm, UnfollowForm
from authentication.models import User
from django.db import IntegrityError
from django.db.models import Q, CharField, Value

# Create your views here.


@login_required
def flux(request):
    """
    Function to display the "flux" page
    """
    tickets = get_users_viewable_tickets(request.user)
    all_reviews = Review.objects.all()
    for review in all_reviews:
        for ticket in tickets:
            if review.ticket == ticket:
                ticket.has_a_reply = True
                ticket.toto = "salut"
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    review = get_users_viewable_reviews(request.user)
    review = review.annotate(content_type=Value("REVIEW", CharField()))

    posts = sorted(
        chain(review, tickets),
        key=lambda post: post.time_created, reverse=True
    )

    context = {
        "posts": posts,
    }
    return render(request, "critics/base_flux.html", context)


@login_required
def add_review(request, ticket_id):
    """
    Function to add a review to a ticket
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    review_form = ReviewForm()
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket  # Add the ticket to the review object
            review.user = request.user  # Add the user to the review object
            review.save()
            return redirect("flux")
    context = {
        "ticket": ticket,
        "review_form": review_form,
    }
    return render(request, "critics/add_review.html", context)


@login_required
def my_posts(request):
    """
    View to display the user posts
    """
    user = request.user
    all_tickets = Ticket.objects.filter(
            user__exact=user).order_by("-time_created")
    my_review = Review.objects.filter(
            user__exact=user).order_by("-time_created")
    all_tickets = all_tickets.annotate(
            content_type=Value("TICKET", CharField()))
    my_review = my_review.annotate(
            content_type=Value("REVIEW", CharField()))
    posts = sorted(
        chain(my_review, all_tickets),
        key=lambda post: post.time_created, reverse=True
    )

    context = {
        "posts": posts,
    }
    return render(request, "critics/my_posts.html", context)


@login_required
def abonnement(request):
    """
    View to display the follow page
    """
    followed_users = UserFollows.objects.filter(
        user=request.user
    )  # Get the followed users list
    unfollow_form = UnfollowForm()  # Create the form to unfollow users
    form = FollowForm()  # Create the form to follow users
    following_users = UserFollows.objects.filter(followed_user=request.user)
    if (
        request.method == "POST" and "follow_form" in request.POST
    ):  # If the user wants to follow someone
        form = FollowForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["followed_user"]
            current_user = request.user
            try:
                user_follow = User.objects.get(username__exact=username)
                if user_follow == current_user:
                    context = {
                        "userfollow_form": form,
                        "feedback":
                        "Vous ne pouvez pas vous suivre vous-même.",
                        "followed_users": followed_users,
                    }
                    return render(request, "critics/abonnement.html", context)

                else:
                    UserFollows.objects.create(
                        user=current_user, followed_user=user_follow
                    )
                    followed_users = UserFollows.objects.filter(
                            user=request.user)
                    following_users = UserFollows.objects.filter(
                        followed_user=request.user
                    )
                    form = FollowForm()
                    context = {
                        "userfollow_form": form,
                        "feedback": "Utilisateur suivi avec succès.",
                        "followed_users": followed_users,
                        "following_users": following_users,
                    }
                    return render(request, "critics/abonnement.html", context)
            except User.DoesNotExist:
                context = {
                    "userfollow_form": form,
                    "feedback": "L'utilisateur n'existe pas.",
                    "followed_users": followed_users,
                }
                return render(request, "critics/abonnement.html", context)
            except IntegrityError:
                context = {
                    "userfollow_form": form,
                    "feedback": "L'utilisateur est déjà suivi.",
                    "followed_users": followed_users,
                }
                return render(request, "critics/abonnement.html", context)
    elif request.method == "POST" and "user_to_unfollow" in request.POST:
        unfollow_form = UnfollowForm(request.POST)
        if unfollow_form.is_valid():
            user_to_unfollow = User.objects.get(
                username=unfollow_form.cleaned_data.get("user_to_unfollow")
            )

            entry_to_delete = UserFollows.objects.filter(
                user=request.user, followed_user=user_to_unfollow
            )

            entry_to_delete.delete()

            followed_users = UserFollows.objects.filter(user=request.user)

            following_users = UserFollows.objects.filter(
                    followed_user=request.user)
            context = {
                "userfollow_form": form,
                "followed_users": followed_users,
                "unfollow_form": unfollow_form,
                "following_users": following_users,
            }
            return render(request, "critics/abonnement.html", context)

    else:
        followed_users = UserFollows.objects.filter(user=request.user)

        unfollow_form = UnfollowForm()
        form = FollowForm()

    context = {
        "userfollow_form": form,
        "followed_users": followed_users,
        "unfollow_form": unfollow_form,
        "following_users": following_users,
    }

    return render(request, "critics/abonnement.html", context)


@login_required
def modify_post(request, ticket_id):
    """
    View to modify a post
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket_form = TicketForm(instance=ticket)
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
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


@login_required
def modify_review(request, review_id):
    """
    View to modify a review
    """
    review = get_object_or_404(Review, id=review_id)
    ticket = review.ticket
    review_form = ReviewForm(instance=review)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user  # Add the user to the review object
            review.save()
            return redirect("my_posts")
    context = {
        "review": review,
        "review_form": review_form,
        "ticket": ticket,
    }
    return render(request, "critics/modify_review.html", context)


@login_required
def delete_post(request, ticket_id):
    """
    Function to delete a post
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.delete()
    return redirect("my_posts")


@login_required
def delete_review(request, review_id):
    """
    Function to delete a review
    """
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    return redirect("my_posts")


class TicketCreateView(LoginRequiredMixin, CreateView):
    """
    Class view to create a ticket
    """
    form_class = TicketForm
    model = Ticket
    success_url = "/flux/"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


@login_required
def create_review(request):
    """
    Function to create a review
    """
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


def get_users_viewable_reviews(user):
    """
    Function to get the reviews a user can have access to depending on the
    users he follows
    """
    followed_users = get_followed_users(user)
    followed_users_id = [followed_user.id for followed_user in followed_users]
    review = Review.objects.filter(
        Q(user=user) | Q(user__id__in=followed_users_id) |
        Q(ticket__user__id=user.id)
    )
    return review


def get_users_viewable_tickets(user):
    """
    Function to get the tickets a user can have access to depending on the
    users he follows
    """
    followed_users = get_followed_users(user)
    followed_users_id = [followed_user.id for followed_user in followed_users]
    tickets = Ticket.objects.filter(
        ~Q(review__user__id=user.id),
        Q(review__isnull=True) | ~Q(review__user__id__in=followed_users_id),
        Q(user=user) | Q(user__id__in=followed_users_id),
    )
    return tickets


def get_following_users(user):
    """
    Function to get the following users a user have
    """
    following_users = UserFollows.objects.filter(followed_user=user)
    following_users_id = [user.id for user in following_users]
    return User.objects.filter(id__in=following_users_id)


def get_followed_users(user):
    """
    Function to get the followed users a user have
    """
    followed_users = UserFollows.objects.filter(user=user)
    followed_users_id = [
        followed_user.followed_user.id for followed_user in followed_users
    ]
    return User.objects.filter(id__in=followed_users_id)
