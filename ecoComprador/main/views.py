from django.shortcuts import render,redirect
import requests, json
from .forms import ProdutoForm,LoginForm
#from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse,JsonResponse

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
    
    
def cadastrarProduto(response):
    form = ProdutoForm()
    context ={
        'form':form
    }
    return render(response,'cadastroProdutos.html',context)


def cadastrarProdutoForm(response):
    if response.method == 'POST':   
        
        form = ProdutoForm(response.POST, response.FILES)
        
        if form.is_valid():
            
            #hadling image upload
            imagem = response.FILES['imagem']
            data = {
                'nome': form.cleaned_data['nome'],
                'dataValid': form.cleaned_data['dataValid'].isoformat(),
                'marca': form.cleaned_data['marca'],
                'peso': float(form.cleaned_data['peso']),
                'quantidade': int(form.cleaned_data['quantidade']),
                'frete': form.cleaned_data['frete'],
                'preco': float(form.cleaned_data['preco'])
            }
            files = {
                'imagem': ('imagem.jpg', imagem.file, 'image/jpeg')  # Example filename and content type
            }
            headers = {}
            
            print("Data to send:", data)  # Debug print
            
            url = 'http://127.0.0.1:8081/api/produto/'
            """for handling images, it will have to go like this, the data in request must be raw, the headers must be empty on content, and the imagefile will be on the beggining"""
            request = requests.post(url=url, data=data,headers=headers,files=files)
            
            print("Response status code:", request.status_code)
            if request.status_code == 201:
                return render(response,'sucesso.html')
            else:
                print(request.text, request.status_code)
                return HttpResponse('<h1>erro no envio para a API</h1>')
        else:
            # Handle invalid form case
            return render(response, 'cadastroProdutos.html', {'form': form, 'error': 'Form data is invalid'})
    else:
        return HttpResponse("invalid request Method",status=405)


def quemSomos(response):
    return render(response,'quemSomos.html')


def login(response):
    form = LoginForm()
    context ={
        'form':form
    }
    return render(response,'login.html',context)


def loginEvent(response):
    if response.method == 'POST':
        form = LoginForm(response.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            data = {
                'username':username,
                'password':password
            }
            
            headers = {}
            url = 'http://127.0.0.1:8081/api/token/'
            request = requests.post(url=url,data=data,headers=headers)
            if request.status_code == 200:
                tokens = request.json()
                response.session['access'] = tokens['access']
                response.session['refresh'] = tokens['refresh']
                return redirect('userInfo')
            else:
                return render(response,'erroCred.html')
            
    else:
        form = LoginForm() 
        

def userInfo(response):
    token = response.session.get('access')
    if not token:
        return redirect('login')

    request = requests.get('http://127.0.0.1:8081/api/protected/userdetail', headers={'Authorization': f'Bearer {token}'})
    if request.status_code == 200:
        userInfo = request.json()
        return render(response,'userInfo.html',{'userInfo':userInfo}) #login succeded
    elif request.status_code == 401:
        refresh_token = response.session.get('refresh')
        if refresh_token:
            refresh_response = requests.post('http://127.0.0.1:8081/api/token/refresh/', data={'refresh': refresh_token})
            if refresh_response.status_code == 200:
                new_tokens = refresh_response.json()
                response.session['access'] = new_tokens['access']
                return userInfo(response)
        return JsonResponse({'error': 'Token expired and refresh failed'}, status=401)
    return JsonResponse({'error': 'Failed to retrieve user info'}, status=400)