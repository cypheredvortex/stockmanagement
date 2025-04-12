from django.db import models
from fournisseur.models import Fournisseur

# Create your models here.
class Commande(models.Model):
    id = models.AutoField(primary_key=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE,null=True, blank=True)  # ForeignKey to Fournisseur
    dateCommande = models.DateField()    
    statut = models.CharField(max_length=20)
    