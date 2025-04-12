from django.db import models

# Create your models here.
class Rapport(models.Model):
    id=models.AutoField(primary_key=True)
    stockId=models.IntegerField()
    DateRapport=models.DateField()
    MouvementDeStock=models.CharField(max_length=20)
    EtatStock=models.CharField(max_length=20)
    Vente=models.CharField(max_length=20)
    Approvisionnement=models.CharField(max_length=20)