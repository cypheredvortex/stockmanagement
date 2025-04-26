from django.db import models

# Create your models here.
class Fournisseur(models.Model):
    id = models.AutoField(primary_key=True)  
    nom = models.CharField(max_length=20)
    contact = models.CharField(max_length=20)
    adresse = models.CharField(max_length=20)

    def __str__(self):
        return str(self.nom)
