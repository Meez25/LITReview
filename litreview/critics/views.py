from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from critics.models import Ticket, Review
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TicketForm, ReviewForm

# Create your views here.


@login_required
def flux(request):
    return render(request, "critics/base_flux.html")


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
    ticket_form = TicketForm()
    review_form = ReviewForm()
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if any([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect("flux")
    context = {
        "ticket_form": ticket_form,
        "review_form": review_form,
    }
    return render(request, "critics/review_form.html", context=context)
