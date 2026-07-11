from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from backend.models import Event, Registration

@login_required
def dashboard_view(request):
    context = {}
    if request.user.is_organizer():
        events = Event.objects.filter(organizer=request.user)
        context['organized_events'] = events
    else:
        registrations = Registration.objects.filter(attendee=request.user).select_related('event')
        context['registrations'] = registrations
    
    return render(request, 'users/dashboard.html', context)
