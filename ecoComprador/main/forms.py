from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    
    class Meta:
        model = Produto
        fields = ['nome','dataValid','marca','peso','quantidade','frete','imagem']
