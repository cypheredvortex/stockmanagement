from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from user.models import UserProfile  # Make sure this matches your app name
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Sum, F, Count
from article.models import Article
from stock.models import Stock
from commande.models import Commande, ArticleCommande
from datetime import timedelta
from django.utils import timezone
import datetime
from collections import defaultdict
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Count
from datetime import datetime, timedelta, date
import json
from article.models import Article
from stock.models import Stock
from commande.models import Commande, ArticleCommande
from rapport.models import Rapport
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.db.models import Q




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


def dashboard_view(request):
    # Total Revenue: Sum of all completed order prices
    total_revenue = Commande.objects.filter(etatCommande='complete').aggregate(Sum('prix'))['prix__sum'] or 0
    
    # Total Orders: Count of all orders
    total_orders = Commande.objects.count()
    
    # Total Stock Quantity: Sum of all article quantities
    total_stock_qty = Article.objects.aggregate(Sum('quantite'))['quantite__sum'] or 0
    
    # Sales Growth: Compare current month's revenue with last month's revenue
    today = date.today()
    first_day_of_this_month = today.replace(day=1)
    first_day_of_last_month = (first_day_of_this_month - timedelta(days=1)).replace(day=1)

    # Calculate current month revenue
    current_month_revenue = Commande.objects.filter(dateCommande__gte=first_day_of_this_month, etatCommande='complete').aggregate(Sum('prix'))['prix__sum'] or 0
    
    # Calculate last month revenue
    last_month_revenue = Commande.objects.filter(dateCommande__gte=first_day_of_last_month, dateCommande__lt=first_day_of_this_month, etatCommande='complete').aggregate(Sum('prix'))['prix__sum'] or 0
    
    # Calculate sales growth
    if last_month_revenue > 0:
        sales_growth = ((current_month_revenue - last_month_revenue) / last_month_revenue) * 100
    else:
        sales_growth = 0

    # Prepare chart data (you might need to adjust this depending on your requirements)
    revenue_data = [
        {"date": "2025-01-01", "revenue": 2000},
        {"date": "2025-02-01", "revenue": 3000},
        {"date": "2025-03-01", "revenue": 2500},
        {"date": "2025-04-01", "revenue": 4000},
    ]
    stock_movements_data = [
        {"date": "2025-01-01", "movement": 100},
        {"date": "2025-02-01", "movement": 150},
        {"date": "2025-03-01", "movement": 120},
        {"date": "2025-04-01", "movement": 180},
    ]
    articles_data = [
        {"nom": "Article 1", "demand": 500},
        {"nom": "Article 2", "demand": 300},
        {"nom": "Article 3", "demand": 150},
        {"nom": "Article 4", "demand": 250},
    ]
    growth_potential_data = [
        {"article": "Article 1", "growth": 50},
        {"article": "Article 2", "growth": 30},
        {"article": "Article 3", "growth": 20},
        {"article": "Article 4", "growth": 40},
    ]

    # Pass data to the template
    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'total_stock_qty': total_stock_qty,
        'sales_growth': sales_growth,
        'revenue_data': revenue_data,
        'stock_movements_data': stock_movements_data,
        'articles_data': articles_data,
        'growth_potential_data': growth_potential_data,
    }
    
    return render(request, 'dashboard.html', context)
