from django.shortcuts import render
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

def update_article_view(request):
    return render(request,'updateArticle.html')
