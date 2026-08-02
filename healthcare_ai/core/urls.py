from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('symptom-checker/', views.symptom_checker, name='symptom_checker'),
    path('health-tips/', views.health_tips, name='health_tips'),
    path('predict/', views.predict, name='predict'),
    path('book-appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('download-prescription/', views.download_prescription, name='download_prescription'),
]
