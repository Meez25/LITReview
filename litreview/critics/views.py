from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from critics.models import Ticket
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


@login_required
def flux(request):
    return render(request, "critics/base_flux.html")


class TicketCreateView(LoginRequiredMixin, CreateView):
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
