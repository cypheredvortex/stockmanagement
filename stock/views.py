from django.shortcuts import render
from django.http import JsonResponse
from stock.models import Stock
# Create your views here.
def get_stocks(request):
    # Fetching all stocks from the database
    stocks = Stock.objects.all()
    
    # Passing the stocks data to the template
    return render(request, 'stocks.html', {'stocks': stocks})