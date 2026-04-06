from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('DOCTOR', 'Doctor'),
        ('RECEPTIONIST', 'Receptionist'),
        ('STAFF', 'Staff'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STAFF')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def is_admin(self):
        return self.role == 'ADMIN'

    def is_doctor(self):
        return self.role == 'DOCTOR'

    def is_receptionist(self):
        return self.role == 'RECEPTIONIST'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
