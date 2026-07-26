from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
import os
import joblib
import numpy as np
from django.conf import settings
from .models import Doctor, Appointment
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def health_tips(request):
    return render(request, 'core/health_tips.html')

def symptom_checker(request):
    try:
        symptoms_path = os.path.join(settings.BASE_DIR, 'trained_model', 'symptoms_list.pkl')
        symptoms_list = joblib.load(symptoms_path)
    except:
        symptoms_list = ['fever', 'cough', 'fatigue', 'headache', 'nausea', 'sore_throat', 'shortness_of_breath', 'chest_pain', 'dizziness']
    
    return render(request, 'core/symptom_checker.html', {'symptoms': symptoms_list})

# Hardcoded Disease Info as per requirements for now (Phase 2)
DISEASE_INFO = {
    'Flu': {'description': 'Influenza is a viral infection that attacks your respiratory system.', 'causes': 'Influenza viruses travel through the air in droplets when someone with the infection coughs, sneezes or talks.', 'risk_factors': 'Age, living conditions, weakened immune system, chronic illnesses.', 'specialist': 'General Physician', 'home_care': 'Rest, drink plenty of fluids, and use over-the-counter pain relievers.', 'medicine': {'usage': 'Antiviral drugs if prescribed early. Acetaminophen for fever.', 'side_effects': 'Nausea, vomiting, dizziness.', 'precautions': 'Avoid giving aspirin to children or teenagers due to risk of Reye\'s syndrome.'}},
    'COVID-19': {'description': 'An infectious disease caused by the SARS-CoV-2 virus.', 'causes': 'Airborne transmission of the virus from infected individuals.', 'risk_factors': 'Older age, underlying medical conditions like heart disease, diabetes, or lung disease.', 'specialist': 'Pulmonologist', 'home_care': 'Isolate, monitor oxygen levels, rest, and stay hydrated.', 'medicine': {'usage': 'Fever reducers, antivirals if prescribed by a doctor.', 'side_effects': 'Varies by medication.', 'precautions': 'Seek emergency care immediately if breathing becomes difficult.'}},
    'Common Cold': {'description': 'A viral infection of your nose and throat (upper respiratory tract).', 'causes': 'Rhinoviruses are the most common cause.', 'risk_factors': 'Age, weakened immune system, time of year (fall/winter), smoking.', 'specialist': 'General Physician', 'home_care': 'Rest, hydration, warm liquids, saltwater gargle.', 'medicine': {'usage': 'Decongestants, pain relievers.', 'side_effects': 'Drowsiness, dry mouth.', 'precautions': 'Do not use over-the-counter cold medicines in children under 4.'}},
    'Migraine': {'description': 'A headache that can cause severe throbbing pain or a pulsing sensation, usually on one side of the head.', 'causes': 'Genetics, environmental factors, changes in the brainstem.', 'risk_factors': 'Family history, age, female gender, stress.', 'specialist': 'Neurologist', 'home_care': 'Rest in a quiet, dark room. Apply cold compresses.', 'medicine': {'usage': 'Pain relievers, triptans.', 'side_effects': 'Nausea, dizziness, drowsiness.', 'precautions': 'Overuse of pain relievers can trigger medication-overuse headaches.'}},
    'Food Poisoning': {'description': 'Illness caused by eating contaminated food.', 'causes': 'Infectious organisms including bacteria, viruses and parasites.', 'risk_factors': 'Older adults, pregnant women, infants and young children, people with chronic disease.', 'specialist': 'Gastroenterologist', 'home_care': 'Let your stomach settle. Drink clear liquids, ease back into eating.', 'medicine': {'usage': 'Anti-diarrhea medications, antibiotics only if bacterial.', 'side_effects': 'Constipation, bloating.', 'precautions': 'Avoid anti-diarrhea meds if you have high fever or bloody stools.'}},
    'Heart Condition': {'description': 'A range of conditions that affect your heart, such as coronary artery disease, arrhythmias, and congenital heart defects.', 'causes': 'Damage to heart muscle/valves, genetics, lifestyle factors.', 'risk_factors': 'Age, sex, family history, smoking, poor diet, high blood pressure.', 'specialist': 'Cardiologist', 'home_care': 'Monitor symptoms closely, rest, avoid stress.', 'medicine': {'usage': 'Statins, beta blockers, ACE inhibitors.', 'side_effects': 'Muscle pain, fatigue, dizziness.', 'precautions': 'Take exactly as prescribed. Do not stop abruptly.'}},
    'Anemia': {'description': 'A condition in which you lack enough healthy red blood cells to carry adequate oxygen to your body\'s tissues.', 'causes': 'Iron deficiency, vitamin deficiency, inflammation, bone marrow diseases.', 'risk_factors': 'A diet lacking in certain vitamins, intestinal disorders, menstruation, pregnancy.', 'specialist': 'Hematologist', 'home_care': 'Eat iron-rich foods, take prescribed supplements.', 'medicine': {'usage': 'Iron supplements, vitamin B12 injections.', 'side_effects': 'Constipation, dark stools, upset stomach.', 'precautions': 'Keep iron supplements out of reach of children (can be highly toxic).'}},
}

def predict(request):
    if request.method == 'POST':
        model_path = os.path.join(settings.BASE_DIR, 'trained_model', 'disease_prediction_model.pkl')
        symptoms_path = os.path.join(settings.BASE_DIR, 'trained_model', 'symptoms_list.pkl')
        
        try:
            model = joblib.load(model_path)
            symptoms_list = joblib.load(symptoms_path)
        except Exception as e:
            return render(request, 'core/symptom_checker.html', {'error': 'Machine learning model not found. Please train the model first.'})

        # Get selected symptoms
        selected_symptoms = request.POST.getlist('symptoms')
        manual_symptoms = request.POST.get('manual_symptoms', '')
        
        if manual_symptoms:
            manual_list = [s.strip().lower().replace(' ', '_') for s in manual_symptoms.split(',')]
            selected_symptoms.extend(manual_list)
            
        # Create input array
        input_data = np.zeros(len(symptoms_list))
        for i, symptom in enumerate(symptoms_list):
            if symptom in selected_symptoms:
                input_data[i] = 1
                
        # Predict
        prediction = model.predict([input_data])[0]
        probabilities = model.predict_proba([input_data])[0]
        confidence = round(max(probabilities) * 100, 2)
        
        # Get details
        details = DISEASE_INFO.get(prediction, {
            'description': 'Information not available.',
            'causes': 'Unknown',
            'risk_factors': 'Unknown',
            'specialist': 'General Physician',
            'home_care': 'Consult a doctor for advice.',
            'medicine': {'usage': 'N/A', 'side_effects': 'N/A', 'precautions': 'N/A'}
        })
        
        # Also pass recommended doctors to context
        specialist_type = details['specialist']
        doctors = Doctor.objects.filter(specialty__icontains=specialist_type)
        if not doctors.exists():
            # fallback if no exact match
            doctors = Doctor.objects.filter(specialty='General Physician')
        
        context = {
            'disease': prediction,
            'confidence': confidence,
            'details': details,
            'doctors': doctors,
            'symptoms_str': ", ".join(selected_symptoms).replace('_', ' ').title()
        }
        
        # Save to session for PDF generation (cannot serialize QuerySet)
        request.session['last_prediction'] = {
            'disease': prediction,
            'confidence': confidence,
            'details': details,
            'symptoms_str': context['symptoms_str']
        }
        
        return render(request, 'core/prediction_result.html', context)
        
    return render(request, 'core/symptom_checker.html')

@login_required(login_url='/login/')
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        reason = request.POST.get('reason')
        
        Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            date=date,
            time=time,
            reason=reason
        )
        messages.success(request, f"Appointment successfully booked with Dr. {doctor.name} on {date} at {time}!")
        return redirect('home')
        
    return render(request, 'core/book_appointment.html', {'doctor': doctor})

def download_prescription(request):
    data = request.session.get('last_prediction')
    if not data:
        messages.warning(request, "No recent diagnosis found. Please run symptom checker first.")
        return redirect('symptom_checker')
        
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 750, "AI Healthcare - Diagnosis Report")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, 700, f"Predicted Condition: {data['disease']} (Confidence: {data['confidence']}%)")
    p.drawString(50, 680, f"Reported Symptoms: {data['symptoms_str']}")
    
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 650, "Medicine Information:")
    p.setFont("Helvetica", 11)
    p.drawString(70, 630, f"Usage: {data['details']['medicine']['usage']}")
    p.drawString(70, 610, f"Side Effects: {data['details']['medicine']['side_effects']}")
    p.drawString(70, 590, f"Precautions: {data['details']['medicine']['precautions']}")
    
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 560, "Recommended Specialist:")
    p.setFont("Helvetica", 11)
    p.drawString(70, 540, data['details']['specialist'])
    
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(50, 500, "DISCLAIMER: This report is generated by an AI model and does not constitute")
    p.drawString(50, 485, "medical advice. Please consult a registered doctor before taking any medication.")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
