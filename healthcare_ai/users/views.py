from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required(login_url='/users/login/')
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.save()
        
        user_profile.age = request.POST.get('age') or None
        user_profile.gender = request.POST.get('gender')
        user_profile.blood_group = request.POST.get('blood_group')
        user_profile.height = request.POST.get('height') or None
        user_profile.weight = request.POST.get('weight') or None
        user_profile.medical_history = request.POST.get('medical_history')
        user_profile.allergies = request.POST.get('allergies')
        user_profile.current_medications = request.POST.get('current_medications')
        user_profile.phone_number = request.POST.get('phone_number')
        user_profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
        
    return render(request, 'users/profile.html', {'profile': user_profile})
