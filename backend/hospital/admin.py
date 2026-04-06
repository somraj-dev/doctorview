from django.contrib import admin
from .models import Department, Doctor, Patient, Appointment, Report, BillingRecord, Contact

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'specialization', 'status']
    list_filter = ['department', 'status']

class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'patient_id', 'department', 'status', 'admission_date']
    search_fields = ['first_name', 'last_name', 'patient_id']
    list_filter = ['status', 'department']

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'date', 'time', 'status']
    list_filter = ['status', 'date']

class ReportAdmin(admin.ModelAdmin):
    list_display = ['patient', 'report_type', 'priority', 'is_completed', 'date']
    list_filter = ['priority', 'is_completed']

class BillingRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'category', 'amount', 'date']
    list_filter = ['category', 'date']

admin.site.register(Department)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(BillingRecord, BillingRecordAdmin)
admin.site.register(Contact)
