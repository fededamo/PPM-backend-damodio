from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('attendee', 'Attendee'),
        ('organizer', 'Organizer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='attendee')

    def is_organizer(self):
        return self.role == 'organizer' or self.is_superuser
