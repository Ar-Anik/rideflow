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


class VehicleType(models.TextChoices):
    CAR = 'car', 'Car'
    MOTORCYCLE = 'motorcycle', 'Motorcycle'
    AUTO_RICKSHAW = 'auto-rickshaw', 'Auto-Rickshaw'


class RideCategory(models.TextChoices):
    CAR_STANDARD = 'car_standard', 'Car Standard'
    CAR_COMFORT = 'car_comfort', 'Car Comfort'
    CAR_XL = 'car_xl', 'Car XL'
    BIKE = 'bike', 'Bike'
    CNG = 'cng', 'CNG'


class Vehicle(TimeStampedModel):

    driver = models.ForeignKey(
        DriverProfile,
        on_delete=models.CASCADE,
        related_name='vehicles',
    )

    vehicle_type = models.CharField(
        max_length=50,
        choices=VehicleType.choices,
    )

    ride_category = models.CharField(
        max_length=50,
        choices=RideCategory.choices,
    )

    brand = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=100, unique=True)
    manufacturing_year = models.PositiveIntegerField()
    passenger_capacity = models.PositiveIntegerField(help_text='Maximum number of passengers, excluding the driver.')
    color = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

        indexs = [
            models.Index(
                fields=['driver', 'is_active'],
                name="veh_driver_active_idx",
            )
        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(
                    vehicle_type=VehicleType.CAR,
                    ride_category__in=[
                        RideCategory.CAR_STANDARD,
                        RideCategory.CAR_COMFORT,
                        RideCategory.CAR_XL,
                    ]
                ) | Q(
                    vehicle_type=VehicleType.MOTORCYCLE,
                    ride_category__in=RideCategory.BIKE
                ) | Q(
                    vehicle_type=VehicleType.AUTO_RICKSHAW,
                    ride_category__in=RideCategory.CNG
                )
            ),

            models.CheckConstraint(
                condition=models.Q(passenger_capacity__gt=0),
                name="passenger_capacity_gt_0",
            ),
        ]

    def __str__(self):
        return f'{self.brand}-{self.model_name} ({self.plate_number})'


class Status(models.TextChoices):
    OFFLINE = 'offline', 'Offline',
    ONLINE = 'online', 'Online',
    ON_TRIP = 'on_trip', 'On Trip',


class DriverAvailability(TimeStampedModel):
    driver = models.OneToOneField(
        'drivers.DriverProfile',
        on_delete=models.CASCADE,
        related_name='driver_availability',
    )

    selected_vehicle = models.ForeignKey(
        'drivers.Vehicle',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='active_for_drivers',
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OFFLINE,
    )

    def __str__(self):
        return f'{self.driver}'


class DocuementType(models.TextChoices):
    DRIVING_LICENSE = "driving_license", "Driving License"
    NATIONAL_ID = "national_id", "National ID"
    PASSPORT = "passport", "Passport"
    BACKGROUND_CHECK = "background_check", "Background Check"


class DocuementStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"


class DriverDocument(TimeStampedModel):
    driver = models.ForeignKey(
        DriverProfile,
        on_delete=models.CASCADE,
        related_name='documents',
    )

    document_type = models.CharField(
        max_length=30,
        choices=DocuementType.choices,
    )

    document_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    file = models.FileField(
        upload_to='driver_documents/',
    )

    expires_at = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=DocuementStatus.choices,
        default=DocuementStatus.PENDING,
    )

    rejection_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.driver_id} - {self.document_type}'

