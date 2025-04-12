from django.db import models
from fournisseur.models import Fournisseur
# Create your models here.
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=20)
    reference = models.CharField(max_length=20)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantiteInitiale = models.IntegerField()
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE,null=True, blank=True)
