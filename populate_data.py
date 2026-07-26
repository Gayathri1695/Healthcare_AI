import os
import django
from datetime import date, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_health.settings')
django.setup()

from core.models import Patient, Appointment, AIDiagnosis

def populate():
    # Clear existing data
    Patient.objects.all().delete()
    
    # Create Patients
    p1 = Patient.objects.create(first_name="John", last_name="Smith", date_of_birth=date(1980, 5, 12), gender="Male", contact_number="555-0100", medical_history="Hypertension")
    p2 = Patient.objects.create(first_name="Emily", last_name="Davis", date_of_birth=date(1992, 8, 24), gender="Female", contact_number="555-0101", medical_history="Asthma")
    p3 = Patient.objects.create(first_name="Michael", last_name="Johnson", date_of_birth=date(1975, 11, 30), gender="Male", contact_number="555-0102", medical_history="Diabetes Type 2")
    
    # Create Diagnostics
    AIDiagnosis.objects.create(patient=p1, test_type="ECG", result_summary="High probability of arrhythmia detected in recent ECG.", probability_score=0.92, requires_attention=True)
    AIDiagnosis.objects.create(patient=p2, test_type="Lung Scan", result_summary="Scan shows anomalies consistent with early-stage pneumonia.", probability_score=0.85, requires_attention=True)
    AIDiagnosis.objects.create(patient=p3, test_type="Blood Work", result_summary="Analysis indicates elevated risk for diabetes progression.", probability_score=0.78, requires_attention=False)
    
    # Create Appointments
    now = timezone.now()
    Appointment.objects.create(patient=p2, datetime=now + timedelta(days=1, hours=2), appointment_type="Follow-up - General Checkup", status="Scheduled")
    Appointment.objects.create(patient=p3, datetime=now + timedelta(days=1, hours=4), appointment_type="Consultation - Cardiology", status="Scheduled")

if __name__ == '__main__':
    populate()
    print("Database populated successfully with mock data.")
