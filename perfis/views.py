from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from perfis.models import Perfil
from django.contrib import messages

# Create your views here.

# Páginas
@login_required(login_url='login')
def index(request):
    dados = {}
    dados['perfis'] = Perfil.objects.all()
    dados['perfil_logado'] = request.user.perfil
    timeline = selecionar_posts_de_amigos(request)  # Recolhendo os posts postados por amigos
    paginator = Paginator(timeline, 15)  # Organiza os posts dos amigos, limitando a 15 por página
    page = request.GET.get('pagina')

    try:
        dados['timeline'] = paginator.page(page)  # Recebe os dados da Pagina pré-definidos em variaveis anteriores
    except Exception: # Em caso de exceção:
        dados['timeline'] = paginator.page(1)
        if page is not None:
            messages.add_message(request, messages.INFO, 'A página {} não existe'.format(page))
    
    return render(request, 'index.html', dados)

# Métodos auxiliares
def selecionar_posts_de_amigos(request):
    perfil_logado = request.user.perfil
    amigos = perfil_logado.contatos.all()
    posts = []
    for amigo in amigos:
        posts.extend(list(amigo.posts.all()))
    posts.sort(key=lambda x: x.data_postagem, reverse=True)
    return posts