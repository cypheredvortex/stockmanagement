from django.shortcuts import render
from django.shortcuts import get_object_or_404
from article.models import Article
from stock.models import Stock
from rapport.models import Rapport

# Create your views here.
def home_view(request):
    return render(request, 'homepage.html')

def article_view(request):
    return render(request, 'articles.html')

def stock_view(request):
    return render(request, 'stocks.html')

def loginpage_view(request):
    return render(request, 'loginpage.html')

def signuppage_view(request):
    return render(request, 'signup.html')

def fournisseur_view(request):
    return render(request,'fournisseur.html')

def commands_view(request):
    return render(request,'commandes.html')

def rapport_view(request):
    return render(request,'rapports.html')

def gestionnaire_view(request):
    return render(request,'gestionnaire.html')

def employe_view(request):
    return render(request,'employe.html')

def liststocks_view(request):
    return render(request,'liststocks.html')    

def listarticles_view(request):
    return render(request,'listarticles.html')

def listcommands_view(request):
    return render(request,'listcommands.html')

def update_article_view(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'article_form.html', {'article': article})

def update_stock_view(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    return render(request, 'stock_form.html', {'stock': stock})

def update_rapport_view(request, pk):
    rapport = get_object_or_404(Rapport, pk=pk)
    return render(request, 'rapport_form.html', {'rapport': rapport})
