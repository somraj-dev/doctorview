import csv
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.http import HttpResponse, JsonResponse
from .models import Patient, Doctor, Appointment, Report, Department, BillingRecord, Contact
from .utils import get_billing_insights_chart, get_patient_arrival_chart, get_report_completion_chart
from django.utils import timezone
from datetime import timedelta

@login_required
def dashboard_view(request):
    # Overall Stats
    total_patients = Patient.objects.all().count()
    active_patients = Patient.objects.filter(status='ACTIVE').count()
    discharged_patients = Patient.objects.filter(status='DISCHARGED').count()
    
    # Billing Insights (calculated totals)
    billing_stats = BillingRecord.objects.values('category').annotate(total=Sum('amount'))
    total_billing = BillingRecord.objects.all().aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Recent Patients
    recent_patients = Patient.objects.all().order_by('-admission_date')[:10]
    
    # Surgery Stats (mock numbers or from appointments)
    surgeries_count = Appointment.objects.filter(appointment_type='SURGERY').count()
    
    # Charts
    billing_chart = get_billing_insights_chart()
    arrival_chart = get_patient_arrival_chart()
    report_chart = get_report_completion_chart()
    
    context = {
        'total_patients': total_patients,
        'active_patients': active_patients,
        'discharged_patients': discharged_patients,
        'total_billing': total_billing,
        'billing_stats': billing_stats,
        'recent_patients': recent_patients,
        'surgeries_count': surgeries_count,
        'billing_chart': billing_chart,
        'arrival_chart': arrival_chart,
        'report_chart': report_chart,
        'today': timezone.now(),
    }
    return render(request, 'hospital/dashboard.html', context)

# Patient Views
@login_required
def patient_list_view(request):
    patients = Patient.objects.all()
    q = request.GET.get('q')
    if q:
        patients = patients.filter(first_name__icontains=q) | patients.filter(last_name__icontains=q) | patients.filter(patient_id__icontains=q)
    return render(request, 'hospital/patient_list.html', {'patients': patients})

@login_required
def patient_detail_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'hospital/patient_detail.html', {'patient': patient})

@login_required
def patient_create_view(request):
    # Implementation simplified
    if request.method == "POST":
        # Process form
        return redirect('patient_list')
    return render(request, 'hospital/patient_form.html')

# Doctor Views
@login_required
def doctor_list_view(request):
    doctors = Doctor.objects.all()
    return render(request, 'hospital/doctor_list.html', {'doctors': doctors})

@login_required
def doctor_detail_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'hospital/doctor_detail.html', {'doctor': doctor})

def doctor_create_view(request):
    return render(request, 'hospital/doctor_form.html')

# Appointment Views
@login_required
def appointment_list_view(request):
    appointments = Appointment.objects.all().order_by('date', 'time')
    return render(request, 'hospital/appointment_list.html', {'appointments': appointments})

def appointment_create_view(request):
    return render(request, 'hospital/appointment_form.html')

# Report Views
@login_required
def report_list_view(request):
    reports = Report.objects.all()
    return render(request, 'hospital/report_list.html', {'reports': reports})

def report_create_view(request):
    return render(request, 'hospital/report_form.html')

# Other Views
@login_required
def department_list_view(request):
    departments = Department.objects.all()
    return render(request, 'hospital/department_list.html', {'departments': departments})

@login_required
def contact_list_view(request):
    contacts = Contact.objects.all()
    return render(request, 'hospital/contact_list.html', {'contacts': contacts})

@login_required
def settings_view(request):
    return render(request, 'hospital/settings.html')

# Export Views
@login_required
def export_data_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="patient_data.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Patient Name', 'ID Number', 'Admission Date', 'Age', 'Diagnosis', 'Status'])
    
    patients = Patient.objects.all()
    for p in patients:
        writer.writerow([f"{p.first_name} {p.last_name}", p.patient_id, p.admission_date, p.age, p.diagnosis, p.status])
    
    return response

@login_required
def export_report_pdf(request):
    # This would use ReportLab or WeasyPrint
    return HttpResponse("PDF Generation logic placeholder")

# Global Search & Command Palette
@login_required
def global_search_view(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        # Simple search across models
        pts = Patient.objects.filter(first_name__icontains=query) | Patient.objects.filter(last_name__icontains=query)
        docs = Doctor.objects.filter(specialization__icontains=query)
        # ... more
        for p in pts:
            results.append({'title': f"{p.first_name} {p.last_name}", 'url': f"/patients/{p.pk}/", 'type': 'Patient'})
        for d in docs:
            results.append({'title': f"Dr. {d.user.last_name}", 'url': f"/doctors/{d.pk}/", 'type': 'Doctor'})
            
    return JsonResponse({'results': results})
