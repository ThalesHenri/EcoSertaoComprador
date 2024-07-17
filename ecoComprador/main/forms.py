from django import forms
from .models import Produto

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

