from django.shortcuts import render, redirect
from .forms import SignupForm

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def dashboard_view(request):
    user = request.user
    return render(request, 'dashboard.html', {'user': user})
