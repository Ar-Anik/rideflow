from django.db import models
from django.conf import settings

from apps.core.models import TimeStampedModel

class PassengerProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="passenger_profile",
    )

    def __str__(self):
        return f'Passenger: {self.user.email}'



