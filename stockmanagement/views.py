# views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from user.models import User
 
def auth_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print("🔐 Trying to authenticate:")
        print("Username:", username)
        print("Password:", password)

        user = authenticate(request, username=username, password=password)

        print("Authenticated user:", user)

        if user is not None:
            login(request, user)
            print("✅ Logged in:", user.username)

            if user.is_superuser or user.role == 'Admin':
                return redirect('/admin/')
            elif user.role == 'Employe':
                return redirect('/employe')
            elif user.role == 'Gestionnaire de stock':
                return redirect('/dashboard')
            else:
                messages.error(request, "Unknown role.")
                return redirect('/loginpage')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('/loginpage')
    
    return render(request, 'loginpage.html')

 
