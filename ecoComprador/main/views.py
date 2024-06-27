from django.shortcuts import render
import requests

# Create your views here.


def homepage(response):
    resposta = requests.get('http://127.0.0.1:8081/api/produto/')
    if resposta.status_code == 200:
        produtos = resposta.json()
    else:
        produtos = []
    imageBaseUrl= 'http://127.0.0.1:8081'
    context = {
        'produtos': produtos,
        'is_empty': not produtos,  # Add an extra context variable to check if the list is empty
        'imageUrl' : imageBaseUrl
    }
    return render(response, 'index.html', context)
    #return render(response ,'index.html')