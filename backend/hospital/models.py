from django.db import models
from django.conf import settings
from django.utils import timezone

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='doctors')
    specialization = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    availability = models.JSONField(default=dict, help_text="Store availability schedule")
    status = models.CharField(max_length=20, choices=(('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')), default='ACTIVE')

    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username}"

class Patient(models.Model):
    GENDER_CHOICES = (('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other'))
    STATUS_CHOICES = (('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('DISCHARGED', 'Discharged'))
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patient_id = models.CharField(max_length=20, unique=True, default="PT-0001")
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    
    # Clinical info
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='patients')
    assigned_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='patients')
    diagnosis = models.TextField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    room_number = models.CharField(max_length=10, blank=True, null=True)
    
    admission_date = models.DateField(default=timezone.now)
    discharge_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    photo = models.ImageField(upload_to='patients/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'No Show'),
    )
    TYPE_CHOICES = (
        ('CONSULTATION', 'Consultation'),
        ('FOLLOW_UP', 'Follow Up'),
        ('EMERGENCY', 'Emergency'),
        ('SURGERY', 'Surgery'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    appointment_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='CONSULTATION')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    reason = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.date}"

class Report(models.Model):
    STATUS_CHOICES = (('URGENT', 'Urgent'), ('MODERATE', 'Moderate'), ('LOW', 'Low'))
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='reports')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='created_reports')
    report_type = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    summary = models.TextField()
    findings = models.TextField()
    recommendations = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=STATUS_CHOICES, default='LOW')
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Report for {self.patient} - {self.report_type}"

class BillingRecord(models.Model):
    CATEGORY_CHOICES = (
        ('CONSULTATION', 'Consultation'),
        ('SURGERY', 'Surgery'),
        ('DIAGNOSTIC', 'Diagnostic'),
        ('PHARMACY', 'Pharmacy'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='bills')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.category} - {self.amount} for {self.patient}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="e.g. Emergency Contact, Nurse, Staff")
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    is_emergency = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.role})"
