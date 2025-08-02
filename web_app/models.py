from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)  # 👈 new field added for migration test
    MARITAL_CHOICES = (
        ('Single', 'Single'),
        ('Married', 'Married'),
    )

    # Additional fields
    dob = models.DateField(
        blank=True, null=True
    )

    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES,
        blank=True, null=True
    )

    marital_status = models.CharField(
        max_length=10, choices=MARITAL_CHOICES,
        blank=True, null=True
    )

    agree_to_terms = models.BooleanField(default=False)

    # Soft delete flag
    is_deleted = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        """Override default delete: perform soft delete"""
        self.is_deleted = True
        self.save()

    def __str__(self) -> str:
        return str(self.username or "")
