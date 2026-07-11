from django.contrib import admin
from .models import Category, Location, Event, Registration

admin.site.register(Category)
admin.site.register(Location)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'category', 'location', 'organizer')
    list_filter = ('category', 'date', 'organizer')
    search_fields = ('title', 'description')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('attendee', 'event', 'registered_at')
    list_filter = ('event', 'registered_at')
    search_fields = ('attendee__username', 'event__title')
