# Project Structure
'''
healthcare_project/
├── healthcare_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── authentication/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html
│   ├── authentication/
│   │   ├── signup.html
│   │   ├── login.html
│   │   ├── patient_dashboard.html
│   │   └── doctor_dashboard.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
└── media/
    └── profile_pics/
'''

# Project Setup Instructions
'''
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# For Windows
venv\Scripts\activate
# For macOS/Linux
source venv/bin/activate

# Install Django
pip install django
pip install pillow  # For image handling

# Create the Django project
django-admin startproject healthcare_project

# Navigate into the project
cd healthcare_project

# Create the authentication app
python manage.py startapp authentication

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the server
python manage.py runserver
'''

# healthcare_project/settings.py
'''python
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'healthcare_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'healthcare_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login URL
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'login_success'
'''

# healthcare_project/urls.py
'''python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
]

# Add URL patterns for serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''

# authentication/models.py
'''python
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_TYPES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.user.username} ({self.user_type})"
'''

# authentication/forms.py
'''python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    USER_TYPES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=USER_TYPES, required=True)
    profile_picture = forms.ImageField(required=False)
    address_line1 = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    pincode = forms.CharField(max_length=10, required=True)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
'''

# authentication/views.py
'''python
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
'''

# authentication/urls.py
'''python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('login-success/', views.login_success_view, name='login_success'),
    path('patient-dashboard/', views.patient_dashboard_view, name='patient_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard_view, name='doctor_dashboard'),
]
'''

# authentication/admin.py
'''python
from django.contrib import admin
from .models import UserProfile

admin.site.register(UserProfile)
'''

# templates/base.html
'''html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Healthcare System{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <header>
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand" href="{% url 'login' %}">Healthcare System</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav ms-auto">
                        {% if user.is_authenticated %}
                            <li class="nav-item">
                                <span class="nav-link">Welcome, {{ user.first_name }}!</span>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'logout' %}">Logout</a>
                            </li>
                        {% else %}
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'login' %}">Login</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="{% url 'signup' %}">Sign Up</a>
                            </li>
                        {% endif %}
                    </ul>
                </div>
            </div>
        </nav>
    </header>

    <main class="container mt-4">
        {% if messages %}
            <div class="messages">
                {% for message in messages %}
                    <div class="alert alert-{{ message.tags }}">
                        {{ message }}
                    </div>
                {% endfor %}
            </div>
        {% endif %}

        {% block content %}{% endblock %}
    </main>

    <footer class="mt-5 py-3 bg-light text-center">
        <div class="container">
            <p>© 2025 Healthcare System. All rights reserved.</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{% static 'js/script.js' %}"></script>
</body>
</html>
'''

# templates/authentication/signup.html
'''html
{% extends 'base.html' %}

{% block title %}Sign Up - Healthcare System{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h2 class="mb-0">Sign Up</h2>
            </div>
            <div class="card-body">
                <form method="post" enctype="multipart/form-data">
                    {% csrf_token %}
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="id_first_name" class="form-label">First Name</label>
                            {{ form.first_name.errors }}
                            <input type="text" name="first_name" id="id_first_name" class="form-control" required>
                        </div>
                        <div class="col-md-6">
                            <label for="id_last_name" class="form-label">Last Name</label>
                            {{ form.last_name.errors }}
                            <input type="text" name="last_name" id="id_last_name" class="form-control" required>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="id_username" class="form-label">Username</label>
                        {{ form.username.errors }}
                        <input type="text" name="username" id="id_username" class="form-control" required>
                    </div>
                    
                    <div class="mb-3">
                        <label for="id_email" class="form-label">Email</label>
                        {{ form.email.errors }}
                        <input type="email" name="email" id="id_email" class="form-control" required>
                    </div>
                    
                    <div class="mb-3">
                        <label for="id_user_type" class="form-label">User Type</label>
                        {{ form.user_type.errors }}
                        <select name="user_type" id="id_user_type" class="form-select" required>
                            <option value="" selected>Select user type</option>
                            <option value="patient">Patient</option>
                            <option value="doctor">Doctor</option>
                        </select>
                    </div>
                    
                    <div class="mb-3">
                        <label for="id_profile_picture" class="form-label">Profile Picture</label>
                        {{ form.profile_picture.errors }}
                        <input type="file" name="profile_picture" id="id_profile_picture" class="form-control">
                    </div>
                    
                    <div class="mb-3">
                        <label for="id_address_line1" class="form-label">Address Line 1</label>
                        {{ form.address_line1.errors }}
                        <input type="text" name="address_line1" id="id_address_line1" class="form-control" required>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-4">
                            <label for="id_city" class="form-label">City</label>
                            {{ form.city.errors }}
                            <input type="text" name="city" id="id_city" class="form-control" required>
                        </div>
                        <div class="col-md-4">
                            <label for="id_state" class="form-label">State</label>
                            {{ form.state.errors }}
                            <input type="text" name="state" id="id_state" class="form-control" required>
                        </div>
                        <div class="col-md-4">
                            <label for="id_pincode" class="form-label">Pincode</label>
                            {{ form.pincode.errors }}
                            <input type="text" name="pincode" id="id_pincode" class="form-control" required>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="id_password1" class="form-label">Password</label>
                        {{ form.password1.errors }}
                        <input type="password" name="password1" id="id_password1" class="form-control" required>
                        <div class="form-text">Your password must be at least 8 characters long and contain letters and numbers.</div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="id_password2" class="form-label">Confirm Password</label>
                        {{ form.password2.errors }}
                        <input type="password" name="password2" id="id_password2" class="form-control" required>
                    </div>
                    
                    <div class="d-grid gap-2">
                        <button type="submit" class="btn btn-primary">Sign Up</button>
                    </div>
                </form>
                
                <div class="mt-3 text-center">
                    <p>Already have an account? <a href="{% url 'login' %}">Login</a></p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

# templates/authentication/login.html
'''html
{% extends 'base.html' %}

{% block title %}Login - Healthcare System{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h2 class="mb-0">Login</h2>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    
                    <div class="mb-3">
                        <label for="id_username" class="form-label">Username</label>
                        {{ form.username.errors }}
                        <input type="text" name="username" id="id_username" class="form-control" required>
                    </div>
                    
                    <div class="mb-3">
                        <label for="id_password" class="form-label">Password</label>
                        {{ form.password.errors }}
                        <input type="password" name="password" id="id_password" class="form-control" required>
                    </div>
                    
                    <div class="d-grid gap-2">
                        <button type="submit" class="btn btn-primary">Login</button>
                    </div>
                </form>
                
                <div class="mt-3 text-center">
                    <p>Don't have an account? <a href="{% url 'signup' %}">Sign Up</a></p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

# templates/authentication/patient_dashboard.html
'''html
{% extends 'base.html' %}

{% block title %}Patient Dashboard - Healthcare System{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header bg-primary text-white">
        <h2 class="mb-0">Patient Dashboard</h2>
    </div>
    <div class="card-body">
        <div class="row">
            <div class="col-md-4 text-center mb-4">
                {% if user.profile.profile_picture %}
                    <img src="{{ user.profile.profile_picture.url }}" alt="Profile Picture" class="img-fluid rounded-circle mb-3" style="max-width: 200px; max-height: 200px;">
                {% else %}
                    <div class="bg-secondary text-white rounded-circle d-flex align-items-center justify-content-center mb-3" style="width: 200px; height: 200px; margin: 0 auto;">
                        <h1>{{ user.first_name|first }}{{ user.last_name|first }}</h1>
                    </div>
                {% endif %}
                <h3>{{ user.first_name }} {{ user.last_name }}</h3>
                <p class="text-muted">Patient</p>
            </div>
            
            <div class="col-md-8">
                <h4>User Information</h4>
                <table class="table">
                    <tr>
                        <th>Username:</th>
                        <td>{{ user.username }}</td>
                    </tr>
                    <tr>
                        <th>Email:</th>
                        <td>{{ user.email }}</td>
                    </tr>
                    <tr>
                        <th>Address:</th>
                        <td>{{ user.profile.address_line1 }}</td>
                    </tr>
                    <tr>
                        <th>City:</th>
                        <td>{{ user.profile.city }}</td>
                    </tr>
                    <tr>
                        <th>State:</th>
                        <td>{{ user.profile.state }}</td>
                    </tr>
                    <tr>
                        <th>Pincode:</th>
                        <td>{{ user.profile.pincode }}</td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

# templates/authentication/doctor_dashboard.html
'''html
{% extends 'base.html' %}

{% block title %}Doctor Dashboard - Healthcare System{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header bg-success text-white">
        <h2 class="mb-0">Doctor Dashboard</h2>
    </div>
    <div class="card-body">
        <div class="row">
            <div class="col-md-4 text-center mb-4">
                {% if user.profile.profile_picture %}
                    <img src="{{ user.profile.profile_picture.url }}" alt="Profile Picture" class="img-fluid rounded-circle mb-3" style="max-width: 200px; max-height: 200px;">
                {% else %}
                    <div class="bg-secondary text-white rounded-circle d-flex align-items-center justify-content-center mb-3" style="width: 200px; height: 200px; margin: 0 auto;">
                        <h1>{{ user.first_name|first }}{{ user.last_name|first }}</h1>
                    </div>
                {% endif %}
                <h3>Dr. {{ user.first_name }} {{ user.last_name }}</h3>
                <p class="text-muted">Doctor</p>
            </div>
            
            <div class="col-md-8">
                <h4>User Information</h4>
                <table class="table">
                    <tr>
                        <th>Username:</th>
                        <td>{{ user.username }}</td>
                    </tr>
                    <tr>
                        <th>Email:</th>
                        <td>{{ user.email }}</td>
                    </tr>
                    <tr>
                        <th>Address:</th>
                        <td>{{ user.profile.address_line1 }}</td>
                    </tr>
                    <tr>
                        <th>City:</th>
                        <td>{{ user.profile.city }}</td>
                    </tr>
                    <tr>
                        <th>State:</th>
                        <td>{{ user.profile.state }}</td>
                    </tr>
                    <tr>
                        <th>Pincode:</th>
                        <td>{{ user.profile.pincode }}</td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}
'''

# static/css/style.css
'''css
/* Custom styles for the healthcare application */
body {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

main {
    flex: 1;
}

footer {
    margin-top: auto;
}

.card {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
}

.card-header {
    font-weight: bold;
}

/* Profile image styles */
.rounded-circle {
    object-fit: cover;
    border: 3px solid #f8f9fa;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
'''

# static/js/script.js
'''javascript
// Check if password and confirm password match
document.addEventListener('DOMContentLoaded', function() {
    const password1Field = document.getElementById('id_password1');
    const password2Field = document.getElementById('id_password2');
    const form = document.querySelector('form');
    
    if (form && password1Field && password2Field) {
        form.addEventListener('submit', function(e) {
            if (password1Field.value !== password2Field.value) {
                e.preventDefault();
                alert('Passwords do not match!');
                
                // Add error styling
                password1Field.classList.add('is-invalid');
                password2Field.classList.add('is-invalid');
            }
        });
        
        // Reset validation styling when typing
        password1Field.addEventListener('input', function() {
            password1Field.classList.remove('is-invalid');
            password2Field.classList.remove('is-invalid');
        });
        
        password2Field.addEventListener('input', function() {
            password1Field.classList.remove('is-invalid');
            password2Field.classList.remove('is-invalid');
        });
    }
});
'''
