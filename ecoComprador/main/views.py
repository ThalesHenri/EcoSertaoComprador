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
    #token autorization
    #need a erro handling
    access = response.session['access'] 
    headers = {'Authorization': f'Bearer {access}'}
    resposta = requests.get(url='http://127.0.0.1:8081/api/produto/',headers=headers)
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
            
            #token autorization
            access = response.session['access'] 
            
            
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
            headers = {'Authorization': f'Bearer {access}'}
            
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
        cnpj = request.POST['cnpj']
        password = request.POST['password']
        response = requests.post('http://127.0.0.1:8081/api/token/', data={'cnpj': cnpj, 'password': password})
        
        if response.status_code == 200:
            tokens = response.json()
            request.session['access'] = tokens['access']
            request.session['refresh'] = tokens['refresh']
            return redirect('dashboard')
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    # Fetch the refresh token from the session (assuming it is stored there)
    refresh_token = request.session.get('refresh')  
    
    if not refresh_token:
        return redirect('login')

    API_BASE_URL = 'http://127.0.0.1:8081/api/'
    response = requests.post(
        f'{API_BASE_URL}logout/',
        json={'refresh': refresh_token},  # Send refresh token in the request body
        # Removed the Authorization header
    )

    if response.status_code == 205:
        # Clear session and redirect to login
        request.session.flush()
        return redirect('login')
    else:
        # Handle errors if logout failed
        return HttpResponse(f"Logout failed: {response.content.decode()}", status=response.status_code)
    
def dashboard(request):
    token = request.session.get('access')
    refresh_token = request.session.get('refresh')

    if not token:
        return redirect('login')

    api_url = 'http://127.0.0.1:8081/api/protected/userdetail'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        print(user_info)
        return render(request, 'userInfo.html', {'userInfo': user_info})
    elif response.status_code == 401 and refresh_token:
        # Token expired, attempt to refresh
        refresh_response = requests.post('http://127.0.0.1:8081/api/token/refresh/', data={'refresh': refresh_token})

        if refresh_response.status_code == 200:
            new_tokens = refresh_response.json()
            request.session['access'] = new_tokens['access']
            request.session['refresh'] = new_tokens['refresh']
            # Retry fetching user info after refreshing tokens
            headers['Authorization'] = f'Bearer {new_tokens["access"]}'
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                user_info = response.json()
                print(user_info)
                return render(request, 'userInfo.html', {'userInfo': user_info})
            else:
                return JsonResponse({'error': 'Failed to retrieve user info after token refresh'}, status=400)
        else:
            # Refresh token also expired or invalid
            return JsonResponse({'error': 'Token expired and refresh failed'}, status=401)
    else:
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