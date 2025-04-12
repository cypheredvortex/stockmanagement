from django.db import models
from article.models import Article

# Create your models here.
class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE,null=True, blank=True)  # ForeignKey to Article model
    quantiteDisponible = models.IntegerField()
    seuilAlerte = models.IntegerField()