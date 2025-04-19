from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Article
from fournisseur.models import Fournisseur

# Fetching all articles from the database
def get_articles(request):
    articles = Article.objects.all()
    return render(request, 'articles.html', {'articles': articles})

def list_articles(request):
    articles = Article.objects.all()
    return render(request, 'listarticles.html', {
        'articles': articles,
    })

# Create Article
def create_article(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        quantite = request.POST.get('quantite')
        fournisseur_id = request.POST.get('fournisseur')  # Assuming this is passed as an ID

        # Checking if required fields are provided
        if nom and quantite is not None:
            # If no fournisseur is provided, we set it to None
            fournisseur = None
            if fournisseur_id:
                fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)

            # Creating the article
            article = Article.objects.create(
                nom=nom,
                quantite=int(quantite),  # Ensure it's an integer
                fournisseur=fournisseur
            )
            return redirect('article_list')  # Redirect to the article list page
        else:
            # Handle the error if required fields are missing
            return HttpResponse("Missing required fields", status=400)

    return render(request, 'article_form.html')  # Show empty form for GET request

# Update Article
def update_article(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        # Extracting the data from the POST request
        nom = request.POST.get('nom')
        quantite = request.POST.get('quantite')
        fournisseur_id = request.POST.get('fournisseur')

        # If fields are provided, update the article
        if nom and quantite is not None:
            fournisseur = None
            if fournisseur_id:
                fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)

            # Update the article object
            article.nom = nom
            article.quantite = int(quantite)
            article.fournisseur = fournisseur
            article.save()

            return redirect('article_list')  # Redirect to the article list page
        else:
            # Handle the error if required fields are missing
            return HttpResponse("Missing required fields", status=400)

    return render(request, 'article_form.html', {'article': article})

# Delete Article
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        article.delete()
        return redirect('article_list')

    return render(request, 'article_confirm_delete.html', {'article': article})
