from django import forms
from .models import Event

from django.utils import timezone

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'category', 'location', 'poster']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_date(self):
        event_date = self.cleaned_data["date"]
        if event_date <= timezone.now():
            raise forms.ValidationError("La data dell'evento deve essere futura.")
        return event_date
