from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm
from .models import Post
from django.http import Http404
from .models import Post
from .forms import PostForm

def home(request):
    return render(request, 'base.html')

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})    
   
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('posts')
        else:
            return render(request, 'register.html', {'form': form})
        
def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Hi {username.title()}, welcome back!')
                return redirect('home')
        
        # form is not valid or user is not authenticated
        messages.error(request,f'Invalid username or password')
        return render(request,'login.html',{'form': form})

def post_lista(request):
    posts = Post.published.all()
    return render(request, 'blog/post/lista.html', {'posts': posts})

def post_detalhes(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)

    return render(request, 'blog/post/detalhes.html', {'posts': post})

def criar_postagem(request):
    if request.method == 'POST':
        # Processar os dados do formulário POST
        form = PostForm(request.POST)
        if form.is_valid():
            # Criar uma nova postagem com os dados do formulário
            nova_postagem = form.save(commit=False)
            nova_postagem.autor = request.user  # Supondo que o autor seja o usuário logado
            nova_postagem.status = Post.Status.PUBLISHED  # Definir o status como publicado, se desejado
            nova_postagem.save()
            return redirect('blog/post/detalhes.html', post_id=nova_postagem.id)  # Redirecionar para a página de detalhes da postagem

    else:
        # Se o método não for POST, renderize o formulário vazio
        form = PostForm()

    return render(request, 'blog/post/criarPostagem.html', {'form': form})