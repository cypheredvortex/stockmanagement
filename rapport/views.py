from django.shortcuts import render, get_object_or_404, redirect
from .models import Rapport
from datetime import datetime


# Create your views here.
def create_rapport(request):
    if request.method == 'POST':
        stock_id = request.POST.get('stockId')
        date_rapport = request.POST.get('DateRapport')
        mouvement_de_stock = request.POST.get('MouvementDeStock')
        etat_stock = request.POST.get('EtatStock')
        vente = request.POST.get('Vente')
        approvisionnement = request.POST.get('Approvisionnement')

        try:
            # Convert data types
            stock_id = int(stock_id)
            date_rapport = datetime.strptime(date_rapport, '%Y-%m-%d').date()

            # Create the Rapport object
            Rapport.objects.create(
                stockId=stock_id,
                DateRapport=date_rapport,
                MouvementDeStock=mouvement_de_stock,
                EtatStock=etat_stock,
                Vente=vente,
                Approvisionnement=approvisionnement
            )

            return redirect('get_rapports')  # ✅ Make sure this name exists in your urls.py

        except (ValueError, TypeError) as e:
            return render(request, 'rapport_form.html', {
                'error': f"Erreur lors de la soumission : {e}"
            })

    return render(request, 'rapport_form.html')

def get_rapports(request):
    # Fetch all rapport data from the database
    rapports = Rapport.objects.all()

    # Pass the data to the template
    return render(request, 'rapports.html', {'rapports': rapports})

def update_rapport(request, rapport_id):
    # Get the rapport object using the provided rapport_id
    rapport = get_object_or_404(Rapport, id=rapport_id)

    if request.method == 'POST':
        # Fetch the updated data from the POST request and update the rapport
        rapport.stockId = request.POST.get('stockId')
        rapport.DateRapport = request.POST.get('DateRapport')
        rapport.MouvementDeStock = request.POST.get('MouvementDeStock')
        rapport.EtatStock = request.POST.get('EtatStock')
        rapport.Vente = request.POST.get('Vente')
        rapport.Approvisionnement = request.POST.get('Approvisionnement')

        # Save the updated rapport to the database
        rapport.save()

        return redirect('rapport_list')  # Redirect to the rapport list after updating

    return render(request, 'rapport_form.html', {'rapport': rapport})  # Display the form with existing data

# Delete Rapport View
def delete_rapport(request, rapport_id):
    # Get the rapport object using the provided rapport_id
    rapport = get_object_or_404(Rapport, id=rapport_id)

    if request.method == 'POST':
        # Delete the rapport object
        rapport.delete()
        return redirect('rapport_list')  # Redirect to the list after deletion

    return render(request, 'rapport_confirm_delete.html', {'rapport': rapport}) 
