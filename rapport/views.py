from django.shortcuts import render, get_object_or_404, redirect
from .models import Rapport
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Helper to disable caching
def disable_cache(response):
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@never_cache
@login_required(login_url='/loginpage/')
def create_rapport(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')

    if request.method == 'POST':
        stock_id = request.POST.get('stockId')
        date_rapport = request.POST.get('DateRapport')
        mouvement_de_stock = request.POST.get('MouvementDeStock')
        etat_stock = request.POST.get('EtatStock')
        vente = request.POST.get('Vente')
        approvisionnement = request.POST.get('Approvisionnement')

        try:
            stock_id = int(stock_id)
            date_rapport = datetime.strptime(date_rapport, '%Y-%m-%d').date()

            Rapport.objects.create(
                stockId=stock_id,
                DateRapport=date_rapport,
                MouvementDeStock=mouvement_de_stock,
                EtatStock=etat_stock,
                Vente=vente,
                Approvisionnement=approvisionnement
            )

            return redirect('get_rapports')

        except (ValueError, TypeError) as e:
            response = render(request, 'rapport_form.html', {
                'error': f"Erreur lors de la soumission : {e}"
            })
            return disable_cache(response)

    response = render(request, 'rapport_form.html')
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def get_rapports(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')

    rapports = Rapport.objects.all()
    response = render(request, 'rapports.html', {'rapports': rapports})
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def update_rapport(request, rapport_id):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')

    rapport = get_object_or_404(Rapport, id=rapport_id)

    if request.method == 'POST':
        rapport.stockId = request.POST.get('stockId')
        rapport.DateRapport = request.POST.get('DateRapport')
        rapport.MouvementDeStock = request.POST.get('MouvementDeStock')
        rapport.EtatStock = request.POST.get('EtatStock')
        rapport.Vente = request.POST.get('Vente')
        rapport.Approvisionnement = request.POST.get('Approvisionnement')
        rapport.save()
        return redirect('rapport_list')

    response = render(request, 'rapport_form.html', {'rapport': rapport})
    return disable_cache(response)

@never_cache
@login_required(login_url='/loginpage/')
def delete_rapport(request, rapport_id):
    if not request.user.is_authenticated:
        return redirect('/loginpage/')

    rapport = get_object_or_404(Rapport, id=rapport_id)

    if request.method == 'POST':
        rapport.delete()
        return redirect('rapport_list')

    response = render(request, 'rapport_confirm_delete.html', {'rapport': rapport})
    return disable_cache(response)
