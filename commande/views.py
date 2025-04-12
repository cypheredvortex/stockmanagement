from django.shortcuts import render
from django.http import JsonResponse
from commande.models import Commande
# Create your views here.
def get_commands(request):
    # Fetching all commands from the database
    commands = Commande.objects.all()
    
    # Passing the commands data to the template
    return render(request, 'commandes.html', {'commands': commands})