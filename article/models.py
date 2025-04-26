from django.db import models
from django.apps import apps

# Create your models here.
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=20)
    references = models.CharField(max_length=20, null=True, blank=True)
    categorie = models.CharField(max_length=20, null=True, blank=True)
    prix = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    quantite = models.IntegerField(default=0)
    
    # Dynamically fetch the Fournisseur model to avoid circular import
    fournisseur = models.ForeignKey('fournisseur.Fournisseur', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def save(self, *args, **kwargs):    
        super().save(*args, **kwargs)

        if self.quantite < 10:
            print('Stock faible')

        if self.quantite == 0:
            print('Stock vide')

        if self.quantite > 100:
            print('Stock suffisant')

        if self.quantite > 50 and self.quantite < 100:
            print('Stock moyen')
