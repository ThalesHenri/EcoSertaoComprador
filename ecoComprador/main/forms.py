from django import forms
from .models import Produto,Fornecedor,Comprador

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'dataValid', 'marca', 'peso', 'quantidade', 'frete', 'preco', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Produto'}),
            'dataValid': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Validade'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'}),
            'frete': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Frete'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Preço'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
        
class LoginForm(forms.Form):
    username = forms.CharField(label='Username',max_length=100)
    password = forms.CharField(label='PassWord',widget=forms.PasswordInput)       


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome','cnpj','responsavel','cpfResponsavel','password']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Responsável'}),
            'cpfResponsavel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF do Responsável'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        }
    
    
class CompradorForm(forms.ModelForm):
    class Meta:
        model = Comprador
        fields = ['nome','cnpj','responsavel','cpfResponsavel','password']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Responsável'}),
            'cpfResponsavel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF do Responsável'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        }