import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "healthcare_ai.settings")
django.setup()

from core.models import Doctor

doctors_data = [
    {'name': 'Sarah Williams', 'specialty': 'General Physician', 'experience_years': 15, 'contact_email': 'sarah.williams@example.com', 'hospital': 'City Central Hospital'},
    {'name': 'Robert Brown', 'specialty': 'Cardiologist', 'experience_years': 20, 'contact_email': 'robert.brown@example.com', 'hospital': 'Heart Care Institute'},
    {'name': 'Emily Chen', 'specialty': 'Pulmonologist', 'experience_years': 12, 'contact_email': 'emily.chen@example.com', 'hospital': 'Lung Health Center'},
    {'name': 'Michael Davis', 'specialty': 'Neurologist', 'experience_years': 18, 'contact_email': 'michael.davis@example.com', 'hospital': 'Neuro Science Clinic'},
    {'name': 'Jessica Taylor', 'specialty': 'Gastroenterologist', 'experience_years': 10, 'contact_email': 'jessica.taylor@example.com', 'hospital': 'Digestive Health Clinic'},
    {'name': 'William Miller', 'specialty': 'Hematologist', 'experience_years': 14, 'contact_email': 'william.miller@example.com', 'hospital': 'Blood Disorder Institute'},
]

for doc_data in doctors_data:
    Doctor.objects.get_or_create(name=doc_data['name'], defaults=doc_data)

print("Dummy doctors populated successfully!")
