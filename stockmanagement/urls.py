"""
URL configuration for stockmanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from pages.views import home_view
from pages.views import article_view
from pages.views import loginpage_view
from pages.views import stock_view
from pages.views import fournisseur_view
from pages.views import commands_view
from pages.views import rapport_view
from pages.views import gestionnaire_view
from pages.views import employe_view
from pages.views import listarticles_view
from pages.views import listcommands_view
from pages.views import liststocks_view
# from stock.views import get_stocks
# from article.views import get_articles
# from commande.views import get_commands

import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('',home_view,name='home_view'),
    path('articles',article_view,name='articles_view'),
    path('loginpage',loginpage_view,name='loginpage_view'),
    path('stocks',stock_view,name='stocks_view'),
    path('fournisseurs',fournisseur_view,name='fournisseurs_view'),
    path('commands',commands_view,name='commands_view'),
    path('rapports',rapport_view,name='rapports_view'),
    path('gestionnaire',gestionnaire_view,name='gestionnaire_view'),
    path('auth',views.auth_view,name='auth_view'),
    path('employe',employe_view,name='employe_view'),
    path('listarticles',listarticles_view,name='listarticles_view'),
    path('listcommands',listcommands_view,name='listcommands_view'),
    path('liststocks',liststocks_view,name='liststocks_view'),
    
    ]
