from django.db import models
from django.apps import apps

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    # Use apps.get_model to defer the import of the Article model
    article = models.ForeignKey(
        'article.Article',  # Reference Article using a string and app label
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    quantiteDisponible = models.IntegerField()
    seuilAlerte = models.IntegerField()

    def __str__(self):
        return f"Stock for {self.article.nom} (ID: {self.id})"
