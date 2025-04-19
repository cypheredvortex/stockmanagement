# stock/views.py
from django.shortcuts import render, get_object_or_404, redirect
from stock.models import Stock
from article.models import Article

# Main view: renders to stocks.html (full management page)
def get_stocks(request):
    stocks = Stock.objects.all()
    articles = Article.objects.all()
    return render(request, 'stocks.html', {
        'stocks': stocks,
        'articles': articles,
    })

# Partial view: renders to liststocks.html (list-only page)
def list_stocks(request):
    stocks = Stock.objects.all()
    return render(request, 'liststocks.html', {
        'stocks': stocks,
    })

# Create a new stock entry
def create_stock(request):
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
            # Redirect back to the full stocks page
            return redirect('stocks')
        except (ValueError, TypeError, Article.DoesNotExist):
            # On error, re-render with context
            return render(request, 'stocks.html', {
                'stocks': Stock.objects.all(),
                'articles': Article.objects.all(),
                'error': 'Erreur dans les champs du formulaire.'
            })
    # For GET, just show the form/page
    return redirect('stocks')

# Update an existing stock
def update_stock(request, stock_id):
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
            return redirect('stocks')
        except (ValueError, TypeError, Article.DoesNotExist):
            return render(request, 'stocks.html', {
                'stocks': Stock.objects.all(),
                'articles': Article.objects.all(),
                'error': 'Erreur lors de la mise à jour.'
            })
    # If accessed via GET, redirect back
    return redirect('stocks')

# Delete a stock
def delete_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    if request.method == 'POST':
        stock.delete()
    return redirect('stocks')

