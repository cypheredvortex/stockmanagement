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
from fournisseur.models import FournisseurArticle
from rapport.models import Rapport
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.db.models import Q
from django.db.models.functions import TruncMonth





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

from django.db.models import Sum, F, Count, Avg
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from datetime import date, timedelta
import json
from django.core.serializers.json import DjangoJSONEncoder
from historiqueActions.models import HistoriqueActions
from article.models import Article
from fournisseur.models import Fournisseur
from commande.models import ArticleCommande, Commande
from stock.models import Stock
from rapport.models import Rapport
from fournisseur.models import FournisseurArticle

@login_required
def dashboard_view(request):
    today = date.today()
    thirty_days_ago = today - timedelta(days=30)

    # --- Financial Metrics ---
    article_commandes = ArticleCommande.objects.annotate(
        revenue=F('quantite') * F('prix_unitaire')
    )

    total_revenue = article_commandes.aggregate(total=Sum('revenue'))['total'] or 0
    revenue_per_article = article_commandes.values('article__nom').annotate(revenue=Sum('revenue')).order_by('-revenue')[:10]

    revenue_per_category_qs = article_commandes.values('article__categorie').annotate(revenue=Sum('revenue')).order_by('-revenue')
    revenue_per_category = [
        {'categorie': entry['article__categorie'], 'revenue': entry['revenue']}
        for entry in revenue_per_category_qs
    ]

    revenue_per_supplier = article_commandes.values('commande__fournisseur__nom').annotate(
        revenue=Sum(F('quantite') * F('prix_unitaire'))
    ).order_by('-revenue')

    revenue_over_time = article_commandes.annotate(
        month=TruncMonth('commande__dateCommande')
    ).values('month').annotate(total=Sum('revenue')).order_by('month')

    # --- Procurement Metrics ---
    # Cannot calculate purchase_cost directly due to missing 'quantite'
    purchase_cost = 0  # Placeholder

    # supplier_spend also not directly computable without quantity
    supplier_spend = 0  # Placeholder

    # Average purchase price per article
    avg_purchase_price = FournisseurArticle.objects.values('article__nom').annotate(avg_price=Avg('prix_achat'))

    # --- Stock Movement Metrics ---
    total_stock_value = Stock.objects.aggregate(
        val=Sum(F('quantiteDisponible') * F('article__prix'))
    )['val'] or 0

    stock_entries = Stock.objects.filter(type="entree").annotate(
        month=TruncMonth('date')
    ).values('month').annotate(total=Sum('quantiteDisponible')).order_by('month')

    stock_exits = Stock.objects.filter(type="sortie").annotate(
        month=TruncMonth('date')
    ).values('month').annotate(total=Sum('quantiteDisponible')).order_by('month')

    stock_alerts = Stock.objects.filter(etatStock="en_alerte").count()

    # Reorder articles: via Stock model, not Article
    reorder_articles = Stock.objects.filter(quantiteDisponible__lt=F('seuilAlerte')).count()

    top_selling = article_commandes.values('article__nom').annotate(
        qty=Sum('quantite')
    ).order_by('-qty')[:10]

    least_selling = article_commandes.values('article__nom').annotate(
        qty=Sum('quantite')
    ).order_by('qty')[:10]

    total_orders = Commande.objects.count()
    average_order_value = total_revenue / total_orders if total_orders else 0

    orders_over_time = Commande.objects.annotate(
        month=TruncMonth('dateCommande')
    ).values('month').annotate(count=Count('id')).order_by('month')

    # --- Sales Growth ---
    recent_revenue = article_commandes.filter(commande__dateCommande__gte=thirty_days_ago).aggregate(
        recent=Sum('revenue'))['recent'] or 0

    previous_revenue = article_commandes.filter(
        commande__dateCommande__lt=thirty_days_ago
    ).aggregate(prev=Sum('revenue'))['prev'] or 0

    if previous_revenue == 0:
        sales_growth = 100 if recent_revenue > 0 else 0
    else:
        sales_growth = ((recent_revenue - previous_revenue) / previous_revenue) * 100

    # --- User Metrics ---
    reports_by_user = Rapport.objects.values('généré_par__username').annotate(count=Count('id'))
    stock_by_user = Stock.objects.values('utilisateur__username').annotate(count=Count('id'))
    action_logs = HistoriqueActions.objects.filter(
        action__icontains="commande"
    ).values('date_action', 'action', 'utilisateur__username').order_by('-date_action')[:20]

    # --- Context ---
    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'average_order_value': round(average_order_value, 2),
        'total_stock_value': total_stock_value,
        'stock_alerts': stock_alerts,
        'reorder_articles': reorder_articles,
        'sales_growth': round(sales_growth, 2),
        'supplier_spend': supplier_spend,
        'purchase_cost': purchase_cost,
        'revenue_per_article': json.dumps(list(revenue_per_article), cls=DjangoJSONEncoder),
        'revenue_per_category': json.dumps(revenue_per_category, cls=DjangoJSONEncoder),
        'revenue_per_supplier': json.dumps(list(revenue_per_supplier), cls=DjangoJSONEncoder),
        'revenue_over_time': json.dumps(list(revenue_over_time), cls=DjangoJSONEncoder),
        'stock_entries': json.dumps(list(stock_entries), cls=DjangoJSONEncoder),
        'stock_exits': json.dumps(list(stock_exits), cls=DjangoJSONEncoder),
        'top_selling': json.dumps(list(top_selling), cls=DjangoJSONEncoder),
        'least_selling': json.dumps(list(least_selling), cls=DjangoJSONEncoder),
        'orders_over_time': json.dumps(list(orders_over_time), cls=DjangoJSONEncoder),
        'reports_by_user': json.dumps(list(reports_by_user), cls=DjangoJSONEncoder),
        'stock_by_user': json.dumps(list(stock_by_user), cls=DjangoJSONEncoder),
        'action_logs': action_logs,
    }

    return render(request, 'dashboard.html', context)
