from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from user.models import UserProfile  # Make sure this matches your app name
from django.contrib.auth.decorators import login_required


def auth_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print("🔐 Trying to authenticate:")
        print("Username:", username)
        
        user = authenticate(request, username=username, password=password)
        print("Authenticated user:", user)

        if user is not None:
            login(request, user)
            print("✅ Logged in:", user.username)

            try:
                role = user.profile.role  # ✅ Correct access to role
            except UserProfile.DoesNotExist:
                messages.error(request, "User profile not found.")
                return redirect('/loginpage')

            if user.is_superuser or role == 'Admin':
                return redirect('/admin/')
            elif role == 'Employe':
                return redirect('/liststocks')
            elif role == 'Gestionnaire de stock':
                return redirect('/stocks')
            else:
                messages.error(request, "Unknown role.")
                return redirect('/loginpage')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('/loginpage')
    
    return render(request, 'loginpage.html')

  # Redirects to login page if user isn't authenticated
def logout_view(request):
    logout(request)
    return redirect('/loginpage')
