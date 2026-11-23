from django.db import models
from django.conf import settings

from apps.core.models import TimeStampedModel

class DriverProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='driver_profile',
    )

    def __str__(self):
        return f'Driver: {self.user.email}'
