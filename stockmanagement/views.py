from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from user.models import UserProfile  # Make sure this matches your app name
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

def auth_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            try:
                role = user.profile.role
                print("✅ Role detected:", role)
            except Exception as e:
                print("🔥 Profile error:", e)
                messages.error(request, "User profile access error.")
                return redirect('loginpage_view')

            # Just for debugging — log what's going to happen
            if user.is_superuser or role.lower() == 'admin':
                print("➡ Redirecting to: /admin/")
                return redirect('/admin/')
            elif role.lower() == 'employe':
                print("➡ Redirecting to: /liststocks")
                return redirect('/liststocks')
            elif role.lower() == 'gestionnaire de stock':
                print("➡ Redirecting to: /stocks")
                return redirect('/stocks')
            else:
                print("❓ Unknown role:", role)
                messages.error(request, "Unknown role.")
                return redirect('loginpage_view')
        else:
            print("❌ Invalid credentials for:", username)
            messages.error(request, "Invalid credentials.")
            return redirect('loginpage_view')

    return render(request, 'loginpage.html')

  # Redirects to login page if user isn't authenticated
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('loginpage_view')
