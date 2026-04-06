import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from hospital.models import Department, Doctor, Patient, Appointment, Report, BillingRecord, Contact
from faker import Faker
from django.utils import timezone
from datetime import timedelta

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seeds the database with realistic healthcare data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # 1. Create Admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@axiovital.com', 'admin123', role='ADMIN')
            self.stdout.write(self.style.SUCCESS('Admin created: admin/admin123'))

        # 2. Create Departments
        depts = ['Cardiology', 'Gastroenterology', 'General Medicine', 'Neurology', 'Pediatrics', 'Oncology', 'Orthopedics']
        dept_objs = []
        for d in depts:
            obj, created = Department.objects.get_or_create(name=d, description=fake.text(max_nb_chars=100))
            dept_objs.append(obj)

        # 3. Create Doctors
        specializations = ['Cardiologist', 'Gastroenterologist', 'GP', 'Neurologist', 'Pediatrician', 'Oncologist', 'Surgeon']
        doctor_objs = []
        for i in range(15):
            username = f'doctor{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username, f'{username}@hospital.com', 'doctor123', 
                                              first_name=fake.first_name(), last_name=fake.last_name(), role='DOCTOR')
                doc = Doctor.objects.create(
                    user=user,
                    department=random.choice(dept_objs),
                    specialization=random.choice(specializations),
                    bio=fake.paragraph(),
                    status='ACTIVE'
                )
                doctor_objs.append(doc)

        # 4. Create Patients
        patient_objs = []
        diagnoses = ['Hypertension', 'Type 2 Diabetes', 'Acute Gastritis', 'Migraine', 'Asthma', 'Common Cold', 'Back Pain', 'Anemia']
        rooms = [f'{i}' for i in range(101, 500)]
        
        for i in range(50):
            p = Patient.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                patient_id=f'PT-{1000 + i}',
                age=random.randint(18, 85),
                gender=random.choice(['MALE', 'FEMALE']),
                email=fake.email(),
                phone=fake.phone_number()[:15],
                address=fake.address(),
                department=random.choice(dept_objs),
                assigned_doctor=random.choice(doctor_objs),
                diagnosis=random.choice(diagnoses),
                room_number=random.choice(rooms),
                admission_date=timezone.now() - timedelta(days=random.randint(1, 30)),
                status=random.choice(['ACTIVE', 'ACTIVE', 'DISCHARGED'])
            )
            patient_objs.append(p)

        # 5. Create Appointments
        for p in patient_objs:
            for _ in range(random.randint(1, 3)):
                Appointment.objects.create(
                    patient=p,
                    doctor=p.assigned_doctor or random.choice(doctor_objs),
                    department=p.department or random.choice(dept_objs),
                    date=timezone.now().date() + timedelta(days=random.randint(-15, 15)),
                    time=timezone.now().time(),
                    appointment_type=random.choice(['CONSULTATION', 'FOLLOW_UP', 'SURGERY', 'EMERGENCY']),
                    status=random.choice(['SCHEDULED', 'COMPLETED', 'CANCELLED']),
                    reason=fake.sentence()
                )

        # 6. Create Reports
        for p in patient_objs:
            if random.random() > 0.5:
                Report.objects.create(
                    patient=p,
                    doctor=p.assigned_doctor or random.choice(doctor_objs),
                    report_type=random.choice(['Blood Test', 'X-Ray', 'MRI Scan', 'Biopsy', 'ECG']),
                    summary=fake.paragraph(),
                    findings=fake.text(),
                    priority=random.choice(['URGENT', 'MODERATE', 'LOW']),
                    is_completed=random.choice([True, False])
                )

        # 7. Create Billing Records
        for p in patient_objs:
            for _ in range(random.randint(1, 4)):
                BillingRecord.objects.create(
                    patient=p,
                    category=random.choice(['CONSULTATION', 'SURGERY', 'DIAGNOSTIC', 'PHARMACY']),
                    amount=random.uniform(50, 5000),
                    date=timezone.now() - timedelta(days=random.randint(0, 60)),
                    description=fake.sentence(),
                    transaction_id=fake.uuid4()[:8].upper()
                )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
