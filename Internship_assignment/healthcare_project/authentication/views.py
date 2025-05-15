
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, LoginForm
from .models import UserProfile

def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            
            # Create user profile
            profile = UserProfile.objects.create(
                user=user,
                user_type=form.cleaned_data.get('user_type'),
                profile_picture=form.cleaned_data.get('profile_picture'),
                address_line1=form.cleaned_data.get('address_line1'),
                city=form.cleaned_data.get('city'),
                state=form.cleaned_data.get('state'),
                pincode=form.cleaned_data.get('pincode')
            )
            
            # Log the user in
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            
            # Redirect based on user type
            if profile.user_type == 'patient':
                return redirect('patient_dashboard')
            else:
                return redirect('doctor_dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'authentication/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # Redirect based on user type
                try:
                    profile = UserProfile.objects.get(user=user)
                    if profile.user_type == 'patient':
                        return redirect('patient_dashboard')
                    else:
                        return redirect('doctor_dashboard')
                except UserProfile.DoesNotExist:
                    messages.error(request, 'User profile does not exist.')
                    return redirect('login')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'authentication/login.html', {'form': form})

def login_success_view(request):
    """
    Redirect users to the correct dashboard based on their type
    """
    if hasattr(request.user, 'profile'):
        user_type = request.user.profile.user_type
        if user_type == 'patient':
            return redirect('patient_dashboard')
        elif user_type == 'doctor':
            return redirect('doctor_dashboard')
    
    messages.error(request, 'User profile not found. Please log in again.')
    return redirect('login')

@login_required
def patient_dashboard_view(request):
    return render(request, 'authentication/patient_dashboard.html')

@login_required
def doctor_dashboard_view(request):
    return render(request, 'authentication/doctor_dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')