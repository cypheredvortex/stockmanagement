from django.shortcuts import render
from django.http import JsonResponse
from article.models import Article
# Create your views here.
def get_articles(request):
    # Fetching all articles from the database
    articles = Article.objects.all()
    
    # Passing the articles data to the template
    return render(request, 'articles.html', {'articles': articles})
