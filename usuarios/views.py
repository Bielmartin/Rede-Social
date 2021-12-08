from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.models import User
from usuarios.forms import RegistrarUsuarioForm
from perfis.models import Perfil

# Create your views here.

class RegistrarUsuarioView(View):
    template_name = 'usuarios/registrar.html'  # Definindo rota para o template

    def get(self, request):
        return render(request, self.template_name)  # Renderização dos templates
    
    def post(self, request):
        form = RegistrarUsuarioForm(request.Post)
        if form.is_valid():
            dados_form = form.cleaned_data
            usuario = User.objects.create_user(username=dados_form['email'],
                                               email=dados_form['email'],
                                               password=dados_form['senha'])  # 
            
            perfil = Perfil(nome=dados_form['nome'],
                            telefone=dados_form['telefone'],
                            nome_empresa=dados_form['nome_empresa'],
                            usuario=usuario)   # Passando os dados para perfil
            
            perfil.save()