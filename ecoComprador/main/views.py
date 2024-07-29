from django.shortcuts import render,redirect
import requests, json
from .forms import ProdutoForm,LoginForm,FornecedorForm,CompradorForm
#from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse,JsonResponse
from urllib.parse import urlencode

# Create your views here.


def homepage(response):
    return render(response,'homepage.html')


def mostrarProdutos(response):
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


def loginEvent(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cnpj = form.cleaned_data.get('cnpj')
            password = form.cleaned_data.get('password')
            
            if not cnpj or not password:
                print(f"primeiro caso,{cnpj},{password}")
                print(form.errors)
                return render(request, 'erroCred.html', {'error': 'CNPJ and password are required'})
                
            
            data = {
                'cnpj': cnpj,  # Assuming 'username' maps to 'cnpj' for authentication
                'password': password
            }
            
            headers = {}
            url = 'http://127.0.0.1:8081/api/login/'
            response = requests.post(url=url, data=data, headers=headers)
            
            if response.status_code == 200:
                tokens = response.json()
                request.session['access'] = tokens['access']
                request.session['refresh'] = tokens['refresh']
                user_data = {'key': 'value', 'object': 'data'}
                query_string = urlencode(user_data)
                return redirect(f'/userInfo/?{query_string}')
                
            else:
                print('caso 2')
                return render(request, 'erroCred.html')

        else:
            print('caso3')
            return render(request, 'erroCred.html', {'error': 'Invalid form submission'})
        
    else:
        form = LoginForm()
        print('caso4')
        return render(request, 'login.html', {'form': form})

def userInfo(request):
    token = request.session.get('access')
    if not token:
        return redirect('login')

    api_url = 'http://127.0.0.1:8081/api/protected/userdetail'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        return render(request, 'userInfo.html', {'userInfo': user_info})
    elif response.status_code == 401:
        refresh_token = request.session.get('refresh')
        if refresh_token:
            refresh_response = requests.post('http://127.0.0.1:8081/api/token/refresh/', data={'refresh': refresh_token})
            if refresh_response.status_code == 200:
                new_tokens = refresh_response.json()
                request.session['access'] = new_tokens['access']
                request.session['refresh'] = new_tokens['refresh']
                # Retry fetching user info after refreshing tokens
                return userInfo(request)
        return JsonResponse({'error': 'Token expired and refresh failed'}, status=401)
    return JsonResponse({'error': 'Failed to retrieve user info'}, status=400)

def cadastrarFornecedor(response):
    form = FornecedorForm()
    context ={
        'form':form
    }
    return render(response,'cadastrarFornecedor.html',context)


def cadastrarFornecedorForm(response):
    if response.method == 'POST':
        form = FornecedorForm(response.POST)
        if form.is_valid():
            
            nome = form.cleaned_data['nome']
            cnpj = form.cleaned_data['cnpj']
            responsavel = form.cleaned_data['responsavel']
            cpfResponsavel = form.cleaned_data['cpfResponsavel']
            password = form.cleaned_data['password']
            
            
            data = {
                'nome':nome,
                'cnpj':cnpj,
                'responsavel':responsavel,
                'cpfResponsavel':cpfResponsavel,
                'password':password
            }
            
            headers={}
            url = 'http://127.0.0.1:8081/api/fornecedores/'
            request = requests.post(data=data,headers=headers,url=url)
            print("Response status code:", request.status_code)
            if request.status_code == 201:
                return render(response,'sucesso.html')
            else:
                print(request.text, request.status_code)
                return HttpResponse('<h1>erro no envio para a API</h1>')
        else:
            # Handle invalid form case
            return render(response, 'cadastrarFornecedor.html', {'form': form, 'error': 'Form data is invalid'})
    else:
        return HttpResponse("invalid request Method",status=405)
                

def cadastrarComprador(response):
    form = CompradorForm()
    context ={
        'form':form
    }
    return render(response,'cadastrarComprador.html',context)


def cadastrarCompradorForm(response):
    if response.method == 'POST':
        form = CompradorForm(response.POST)
        if form.is_valid():
            
            nome = form.cleaned_data['nome']
            cnpj = form.cleaned_data['cnpj']
            responsavel = form.cleaned_data['responsavel']
            cpfResponsavel = form.cleaned_data['cpfResponsavel']
            password = form.cleaned_data['password']
            
            
            data = {
                'nome':nome,
                'cnpj':cnpj,
                'responsavel':responsavel,
                'cpfResponsavel':cpfResponsavel,
                'password':password
            }
            
            headers={}
            url = 'http://127.0.0.1:8081/api/compradores/'
            request = requests.post(data=data,headers=headers,url=url)
            print("Response status code:", request.status_code)
            if request.status_code == 201:
                return render(response,'sucesso.html')
            else:
                print(request.text, request.status_code)
                return HttpResponse('<h1>erro no envio para a API</h1>')
        else:
            # Handle invalid form case
            return render(response, 'cadastrarFornecedor.html', {'form': form, 'error': 'Form data is invalid'})
    else:
        return HttpResponse("invalid request Method",status=405)