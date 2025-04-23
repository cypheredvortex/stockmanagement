from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages  # For feedback messages
from django.apps import apps


def list_articles(request):
    Article = apps.get_model('article', 'Article')  # Dynamically fetch the Article model
    articles = Article.objects.all()
    return render(request, 'listarticles.html', {
        'articles': articles,
    })


def get_articles(request):
    Article = apps.get_model('article', 'Article')  # Dynamically fetch the Article model
    articles = Article.objects.all()
    return render(request, 'articles.html', {'articles': articles})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.apps import apps

def create_article(request):
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
            return render(request, 'article_form.html')

        try:
            quantite = int(quantite)
        except ValueError:
            messages.error(request, "Quantité must be a valid integer.")
            return render(request, 'article_form.html')

        if prix:
            try:
                prix = float(prix)
            except ValueError:
                messages.error(request, "Prix must be a valid number.")
                return render(request, 'article_form.html')
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

    return render(request, 'article_form.html')


def update_article(request, article_id):
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

    return render(request, 'article_form.html', {'article': article})

def delete_article(request, article_id):
    Article = apps.get_model('article', 'Article')  # Dynamically fetch the Article model
    article = get_object_or_404(Article, pk=article_id)

    if request.method == 'POST':
        article.delete()
        messages.success(request, "Article deleted successfully.")
        return redirect('get_articles')

    return render(request, 'article_confirm_delete.html', {'article': article})
