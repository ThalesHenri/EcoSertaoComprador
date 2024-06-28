from django.urls import path
from . import views



urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('cadastrarProduto/',views.cadastrarProduto,name='cadastrarProduto')
]
