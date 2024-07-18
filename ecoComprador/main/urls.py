from django.urls import path
from . import views



urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('mostrarProdutos/',views.mostrarProdutos,name='mostrarProdutos'),
    path('cadastrarProduto/',views.cadastrarProduto,name='cadastrarProduto'),
    path('cadastrarProduto/sendForm/',views.cadastrarProdutoForm, name='cadastrarProdutoForm'),
    path('cadastrarFornecedor/',views.cadastrarFornecedor,name='cadastrarFornecedor'),
    path('cadastrarFornecedor/sendForm/',views.cadastrarFornecedorForm,name='cadastrarFornecedorForm'),
    path('cadastrarComprador/',views.cadastrarComprador,name='cadastrarComprador'),
    path('cadastrarComprador/sendForm/',views.cadastrarCompradorForm,name='cadastrarCompradorForm'),
    path('quemSomos/',views.quemSomos,name='quemSomos'),
    path('login/',views.login,name='login'),
    path('login/event/',views.loginEvent,name='loginEvent'),
    path('userInfo/',views.userInfo,name='userInfo'), 
    
]
