from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from .forms import LoginForm, RegisterForm
from .models import Post
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
            return redirect('/blog/')
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
                return redirect('/blog/')
        
        # form is not valid or user is not authenticated
        messages.error(request,f'Invalid username or password')
        return render(request,'login.html',{'form': form})
    
def logout_view(request):
    logout(request)
    return redirect('/blog/')

def post_lista(request):
    posts = Post.published.all()
    return render(request, 'blog/post/lista.html', {'posts': posts})

def detalhes_postagem(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)

    return render(request, 'blog/post/detalhes.html', {'post': post})

def criar_postagem(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            nova_postagem = form.save(commit=False)
            nova_postagem.autor = request.user
            nova_postagem.status = Post.Status.PUBLISHED
            nova_postagem.save()
            return redirect('blog:lista_postagens')
    else:
        form = PostForm()

    return render(request, 'blog/post/criarPostagem.html', {'form': form})

def editar_postagem(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.dt_atualizado = timezone.now()
            post.editado = True
            post.save()
            return redirect('blog:detalhes_postagem', id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post/editarPostagem.html', {'form': form, 'post': post})

def confirmar_exclusao(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/post/confirmarExclusao.html', {'post': post})

def deletar_postagem(request, id):
    post = get_object_or_404(Post, id=id)
    
    # Verificar se o usuário é o autor da postagem antes de permitir a exclusão
    if request.user == post.autor:
        post.delete()
    
    return redirect('blog:lista_postagens')