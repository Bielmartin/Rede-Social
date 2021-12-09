from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from perfis.models import Perfil, Convite, Post
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

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

@login_required(login_url='login')
def exibir_perfil(request, perfil_id):  # Renderizador do perfil
    dados = {}
    dados['perfil'] = Perfil.objects.get(id=perfil_id)  # Carregando do banco os dados
    dados['perfil_logado'] = perfil_logado = request.user.perfil  # 
    dados['ja_eh_contato'] = dados['perfil_logado'].contatos.filter(id=dados['perfil'].id)
    dados['timeline'] = dados['perfil'].posts.all() 

    return render(request, 'perfil.html', dados)

@login_required(login_url='login')
def esqueci_a_minha_senha(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        query = Perfil.objects.filter(email=email)  # Verificar se o email é valido
        if len(query) == 0:
            messages.add_message(request, messages.INFO, 'Email não cadastrado')  # Caso não seja um email cadastrado
            return redirect('esqueci_senha')
        else:
            messages.add_message(request, messages.INFO, 'Ainda não feito, Um email foi enviado para você contendo o link de alteração de senha')
            return redirect('login')
    return render(request, 'esqueci_senha.html')

@login_required(login_url='login')
def postagem(request):
    if request.method == 'POST':
        try:
            titulo = request.POST.get('titulo')
            texto = request.POST.get('texto')
            imagem = request.FILES['imagem']
            perfil = request.user.perfil
            
            postagem_valida = True
            if len(titulo) <= 0:  # Para a imagem ser valida:
                messages.add_message(request, messages.INFO, 'O campo de título deve ser preenchido.')
                postagem_valida = False
            if len(texto) <= 0:
                messages.add_message(request, messages.INFO, 'O campo de texto deve ser preenchido.')
            if not postagem_valida:
                return redirect('index')
            else:
                # Formatação de imagem
                file_system = FileSystemStorage()  # FileSystemStorage -> Upload de arquivos
                file_name = file_system.save(imagem.name, imagem)
                # Salvando no banco de dados
                Post.objects.create(titulo=titulo, text=texto, perfil=perfil, imagem=file_name)  # Cria um objeto de Post
                messages.add_message(request, messages.INFO, 'Postagem publicada.')  # Envia uma mensagem de sucesso na ação
                
        except:
            pass

# Métodos auxiliares
def selecionar_posts_de_amigos(request):
    perfil_logado = request.user.perfil
    amigos = perfil_logado.contatos.all()
    posts = []
    for amigo in amigos:
        posts.extend(list(amigo.posts.all()))
    posts.sort(key=lambda x: x.data_postagem, reverse=True)
    return posts