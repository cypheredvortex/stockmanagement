from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages  # For feedback messages
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Helper to disable cache
def disable_cache(response):
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@never_cache
@login_required(login_url='/loginpage/')
def list_articles(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    Article = apps.get_model('article', 'Article')  # Dynamically fetch the Article model
    articles = Article.objects.all()
    response = render(request, 'listarticles.html', {'articles': articles})
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def get_articles(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    Article = apps.get_model('article', 'Article')
    articles = Article.objects.all()
    response = render(request, 'articles.html', {'articles': articles})
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def create_article(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    if request.method == 'POST':
        nom = request.POST.get('nom')
        quantite = request.POST.get('quantite')
        fournisseur_id = request.POST.get('fournisseur')
        references = request.POST.get('references')
        categorie = request.POST.get('categorie')
        prix = request.POST.get('prix')

        # Basic validation
        if not nom or quantite is None:
            messages.error(request, "Nom and Quantité are required.")
            response = render(request, 'article_form.html')
            return disable_cache(response)

        try:
            quantite = int(quantite)
        except ValueError:
            messages.error(request, "Quantité must be a valid integer.")
            response = render(request, 'article_form.html')
            return disable_cache(response)

        if prix:
            try:
                prix = float(prix)
            except ValueError:
                messages.error(request, "Prix must be a valid number.")
                response = render(request, 'article_form.html')
                return disable_cache(response)
        else:
            prix = None

        # Dynamically fetch models
        Fournisseur = apps.get_model('fournisseur', 'Fournisseur')
        Article = apps.get_model('article', 'Article')

        fournisseur = None
        if fournisseur_id:
            fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)

        # Create the article
        Article.objects.create(
            nom=nom,
            quantite=quantite,
            fournisseur=fournisseur,
            references=references,
            categorie=categorie,
            prix=prix
        )

        messages.success(request, "Article created successfully.")
        return redirect('get_articles')

    response = render(request, 'article_form.html')
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def update_article(request, article_id):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    Article = apps.get_model('article', 'Article')
    article = get_object_or_404(Article, pk=article_id)

    if request.method == 'POST':
        nom = request.POST.get('nom')
        quantite = request.POST.get('quantite')
        fournisseur_id = request.POST.get('fournisseur')
        references = request.POST.get('references')
        categorie = request.POST.get('categorie')
        prix = request.POST.get('prix')

        print("POST Data:", nom, quantite, fournisseur_id, references, categorie, prix)

        if nom and quantite is not None:
            Fournisseur = apps.get_model('fournisseur', 'Fournisseur')
            fournisseur = None
            if fournisseur_id:
                fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)

            # Update fields
            article.nom = nom
            article.quantite = int(quantite)
            article.fournisseur = fournisseur
            article.references = references or None
            article.categorie = categorie or None

            # Convert prix to float if provided
            if prix:
                try:
                    article.prix = float(prix)
                except ValueError:
                    return HttpResponse("Prix invalide", status=400)

            article.save()
            print("Article updated successfully:", article)
            return redirect('get_articles')
        else:
            return HttpResponse("Champs requis manquants", status=400)

    response = render(request, 'article_form.html', {'article': article})
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def delete_article(request, article_id):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')
    Article = apps.get_model('article', 'Article')
    article = get_object_or_404(Article, pk=article_id)

    if request.method == 'POST':
        article.delete()
        messages.success(request, "Article deleted successfully.")
        return redirect('get_articles')

    response = render(request, 'article_confirm_delete.html', {'article': article})
    return disable_cache(response)
