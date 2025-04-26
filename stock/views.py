# stock/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from article.models import Article
from stock.models import Stock

# Helper to disable caching
def disable_cache(response):
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@never_cache
@login_required(login_url='/loginpage/')
def get_stocks(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')

    Stock = apps.get_model('stock', 'Stock')
    Article = apps.get_model('article', 'Article')

    stocks = Stock.objects.all()
    articles = Article.objects.all()

    response = render(request, 'stocks.html', {
        'stocks': stocks,
        'articles': articles,
    })
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def get_stock_form(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')

    Stock = apps.get_model('stock', 'Stock')
    Article = apps.get_model('article', 'Article')

    stocks = Stock.objects.all()
    articles = Article.objects.all()

    response = render(request, 'stock_form.html', {  # <--- here 'stock_form.html'
        'stocks': stocks,
        'articles': articles,
    })
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def list_stocks(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')

    Stock = apps.get_model('stock', 'Stock')

    stocks = Stock.objects.all()
    response = render(request, 'liststocks.html', {
        'stocks': stocks,
    })
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def create_stock(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')

    Stock = apps.get_model('stock', 'Stock')
    Article = apps.get_model('article', 'Article')

    if request.method == 'POST':
        article_id = request.POST.get('article')
        quantite = request.POST.get('quantite')
        seuilAlerte = request.POST.get('seuilAlerte')

        try:
            article = Article.objects.get(id=article_id)
            quantite = int(quantite)
            seuilAlerte = int(seuilAlerte)

            Stock.objects.create(
                article=article,
                quantiteDisponible=quantite,
                seuilAlerte=seuilAlerte
            )

            return redirect('get_stocks')

        except (ValueError, TypeError, Article.DoesNotExist):
            response = render(request, 'stocks.html', {
                'stocks': Stock.objects.all(),
                'articles': Article.objects.all(),
                'error': 'Erreur dans les champs du formulaire.'
            })
            return disable_cache(response)

    response = render(request, 'stocks.html', {
        'stocks': Stock.objects.all(),
        'articles': Article.objects.all()
    })
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def update_stock(request, stock_id):
    Stock = apps.get_model('stock', 'Stock')
    Article = apps.get_model('article', 'Article')

    stock = get_object_or_404(Stock, id=stock_id)

    if request.method == 'POST':
        article_id = request.POST.get('article')
        quantite = request.POST.get('quantite')
        seuilAlerte = request.POST.get('seuilAlerte')

        try:
            article = Article.objects.get(id=article_id)
            quantite = int(quantite)
            seuilAlerte = int(seuilAlerte)

            # Update the stock object
            stock.article = article
            stock.quantiteDisponible = quantite
            stock.seuilAlerte = seuilAlerte
            stock.save()

            return redirect('get_stocks')

        except (ValueError, TypeError, Article.DoesNotExist):
            response = render(request, 'stocks.html', {
                'stocks': Stock.objects.all(),
                'articles': Article.objects.all(),
                'error': 'Erreur dans les champs du formulaire.'
            })
            return disable_cache(response)

    # Handle GET request (user opens the edit page)
    response = render(request, 'stock_form.html', {
        'stocks': Stock.objects.all(),
        'articles': Article.objects.all(),
        'stock': stock,
        'article': stock.article
    })
    return disable_cache(response)


@never_cache
@login_required(login_url='/loginpage/')
def delete_stock(request, stock_id):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')

    Stock = apps.get_model('stock', 'Stock')

    stock = get_object_or_404(Stock, id=stock_id)
    if request.method == 'POST':
        stock.delete()
    return redirect('get_stocks')
