from django.shortcuts import render, get_object_or_404, redirect
from .models import Rapport

# Create your views here.
def create_rapport(request):
    if request.method == 'POST':
        stock_id = request.POST.get('stockId')
        date_rapport = request.POST.get('DateRapport')
        mouvement_de_stock = request.POST.get('MouvementDeStock')
        etat_stock = request.POST.get('EtatStock')
        vente = request.POST.get('Vente')
        approvisionnement = request.POST.get('Approvisionnement')

        # Creating the new Rapport object
        rapport = Rapport.objects.create(
            stockId=stock_id,
            DateRapport=date_rapport,
            MouvementDeStock=mouvement_de_stock,
            EtatStock=etat_stock,
            Vente=vente,
            Approvisionnement=approvisionnement
        )
        return redirect('rapport_list')  # Redirect to the list of rapports after creation

    return render(request, 'rapport_form.html')  # Show the form for GET requests

def get_rapports(request):
    # Fetch all rapport data from the database
    rapports = Rapport.objects.all()

    # Pass the data to the template
    return render(request, 'rapports.html', {'rapports': rapports})

def update_rapport(request, pk):
    rapport = get_object_or_404(Rapport, pk=pk)  # Get the rapport object by primary key

    if request.method == 'POST':
        # Fetch the updated data from the POST request
        rapport.stockId = request.POST.get('stockId')
        rapport.DateRapport = request.POST.get('DateRapport')
        rapport.MouvementDeStock = request.POST.get('MouvementDeStock')
        rapport.EtatStock = request.POST.get('EtatStock')
        rapport.Vente = request.POST.get('Vente')
        rapport.Approvisionnement = request.POST.get('Approvisionnement')

        # Save the updated rapport to the database
        rapport.save()

        return redirect('rapport_list')  # Redirect to the list after saving

    return render(request, 'rapport_form.html', {'rapport': rapport})  # Show the form with existing data

# Delete Rapport
def delete_rapport(request, pk):
    rapport = get_object_or_404(Rapport, pk=pk)  # Get the rapport object by primary key

    if request.method == 'POST':
        rapport.delete()  # Delete the rapport object
        return redirect('rapport_list')  # Redirect to the list after deletion

    return render(request, 'rapport_confirm_delete.html', {'rapport': rapport})  # Confirm deletion page
