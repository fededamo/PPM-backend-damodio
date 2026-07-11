from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from backend.models import Category, Location, Event, Registration
from django.utils.timezone import now
import datetime

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with initial demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing old data...')
        Registration.objects.all().delete()
        Event.objects.all().delete()
        Location.objects.all().delete()
        Category.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write('Creating superuser...')
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')

        self.stdout.write('Creating test users...')
        org_user = User.objects.create_user(username='org_demo', email='org@example.com', password='password123', role='organizer')
        att_user = User.objects.create_user(username='att_demo', email='att@example.com', password='password123', role='attendee')

        self.stdout.write('Creating categories and locations...')
        cat1 = Category.objects.create(name='Technology')
        cat2 = Category.objects.create(name='Music')
        
        loc1 = Location.objects.create(name='Main Hall', address='123 Tech Street, Silicon Valley')
        loc2 = Location.objects.create(name='Central Park', address='New York, NY')

        self.stdout.write('Creating events...')
        evt1 = Event.objects.create(
            title='AI Summit 2026',
            description='The largest AI conference of the year.',
            date=now() + datetime.timedelta(days=30),
            category=cat1,
            location=loc1,
            organizer=org_user
        )
        
        evt2 = Event.objects.create(
            title='Summer Open Air Concert',
            description='Live music in the park.',
            date=now() + datetime.timedelta(days=15),
            category=cat2,
            location=loc2,
            organizer=org_user
        )

        self.stdout.write('Registering attendee...')
        Registration.objects.create(attendee=att_user, event=evt1)

        self.stdout.write(self.style.SUCCESS('Successfully populated database with demo data.'))
