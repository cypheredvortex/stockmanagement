from django.db import models

# Create your models here.
class Fournisseur(models.Model):
    id = models.AutoField(primary_key=True)  # Use AutoField instead of IntegerField
    nom = models.CharField(max_length=20)
    contact = models.CharField(max_length=20)
    adresse = models.CharField(max_length=20)