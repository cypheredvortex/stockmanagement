# stock/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.apps import apps

# Main view: renders to stocks.html (full management page)
def get_stocks(request):
    # Dynamically fetch models using apps.get_model to avoid circular import
    Stock = apps.get_model('stock', 'Stock')
    Article = apps.get_model('article', 'Article')

    stocks = Stock.objects.all()
    articles = Article.objects.all()

    return render(request, 'stocks.html', {
        'stocks': stocks,
        'articles': articles,
    })

# Partial view: renders to liststocks.html (list-only page)
def list_stocks(request):
    # Dynamically fetch Stock model
    Stock = apps.get_model('stock', 'Stock')

    stocks = Stock.objects.all()
    return render(request, 'liststocks.html', {
        'stocks': stocks,
    })

# Create a new stock entry
def create_stock(request):
    # Dynamically fetch models
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

            return redirect('get_stocks')  # ✅ Assuming 'get_stocks' is the valid name

        except (ValueError, TypeError, Article.DoesNotExist):
            return render(request, 'stocks.html', {
                'stocks': Stock.objects.all(),
                'articles': Article.objects.all(),
                'error': 'Erreur dans les champs du formulaire.'
            })

    # For GET request
    return render(request, 'stocks.html', {
        'stocks': Stock.objects.all(),
        'articles': Article.objects.all()
    })

# Update an existing stock
def update_stock(request, stock_id):
    # Dynamically fetch Stock and Article models
    Stock = apps.get_model('stock', 'Stock')
    Article = apps.get_model('article', 'Article')

    stock = get_object_or_404(Stock, id=stock_id)
    if request.method == 'POST':
        article_id = request.POST.get('article')
        quantite = request.POST.get('quantite')
        seuilAlerte = request.POST.get('seuilAlerte')

        try:
            stock.article = Article.objects.get(id=article_id)
            stock.quantiteDisponible = int(quantite)
            stock.seuilAlerte = int(seuilAlerte)
            stock.save()
            return redirect('get_stocks')

        except (ValueError, TypeError, Article.DoesNotExist):
            return render(request, 'stocks.html', {
                'stocks': Stock.objects.all(),
                'articles': Article.objects.all(),
                'error': 'Erreur lors de la mise à jour.'
            })

    # If accessed via GET, redirect back
    return redirect('get_stocks')

# Delete a stock
def delete_stock(request, stock_id):
    # Dynamically fetch Stock model
    Stock = apps.get_model('stock', 'Stock')

    stock = get_object_or_404(Stock, id=stock_id)
    if request.method == 'POST':
        stock.delete()
    return redirect('get_stocks')
