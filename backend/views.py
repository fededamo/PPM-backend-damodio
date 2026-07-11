from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import EventForm
from .models import Event, Registration


class EventListView(ListView):
    model = Event
    template_name = "backend/event_list.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.select_related("category", "location", "organizer").order_by("date")


class EventDetailView(DetailView):
    model = Event
    template_name = "backend/event_detail.html"
    context_object_name = "event"

    def get_queryset(self):
        return Event.objects.select_related("category", "location", "organizer")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["is_registered"] = (
            user.is_authenticated
            and Registration.objects.filter(attendee=user, event=self.object).exists()
        )
        context["attendees"] = self.object.registrations.select_related("attendee").all()
        return context


class OrganizerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_organizer()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, "Non hai i permessi per eseguire questa operazione.")
        return redirect("backend:event_list")


class EventCreateView(OrganizerRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "backend/event_form.html"

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, "Evento creato correttamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("backend:event_detail", kwargs={"pk": self.object.pk})


class OwnerRequiredMixin(OrganizerRequiredMixin):
    def test_func(self):
        return super().test_func() and self.get_object().organizer_id == self.request.user.id


class EventUpdateView(OwnerRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "backend/event_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Evento aggiornato correttamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("backend:event_detail", kwargs={"pk": self.object.pk})


class EventDeleteView(OwnerRequiredMixin, DeleteView):
    model = Event
    template_name = "backend/event_confirm_delete.html"
    success_url = reverse_lazy("users:dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Evento eliminato correttamente.")
        return super().form_valid(form)


@login_required
@require_POST
def register_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.user.is_organizer():
        messages.error(request, "Gli organizzatori non possono iscriversi agli eventi.")
        return redirect("backend:event_detail", pk=pk)

    _, created = Registration.objects.get_or_create(attendee=request.user, event=event)
    if created:
        messages.success(request, "Iscrizione completata.")
    else:
        messages.info(request, "Sei già iscritto a questo evento.")
    return redirect("backend:event_detail", pk=pk)


@login_required
@require_POST
def unregister_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    deleted, _ = Registration.objects.filter(attendee=request.user, event=event).delete()

    if deleted:
        messages.success(request, "Iscrizione annullata.")
    else:
        messages.info(request, "Non eri iscritto a questo evento.")
    return redirect("backend:event_detail", pk=pk)
