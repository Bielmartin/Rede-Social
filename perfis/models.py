from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Perfil(models.Model):
    nome = models.CharField(max_length=255, null=False)
    imagem_perfil = models.ImageField(null=True, blank=True, upload_to='uploads/fotoperfil/')
    telefone = models.CharField(max_length=15, null= False)
    contatos = models.ManyToManyField('self')
    usuario = models.OneToOneField(User, related_name='perfil', on_delete=models.CASCADE)

    def convidar(self, perfil_convidado):
        convite = Convite(solicitante=self,convidado = perfil_convidado)
        convite.save()

    def desfazer_amizade(self, perfil_amizade):
        self.contatos.remove(perfil_amizade.id)
        
class Convite(models.Model):
    solicitante = models.ForeignKey(Perfil,on_delete=models.CASCADE,related_name='convites_feitos' )
    convidado = models.ForeignKey(Perfil, on_delete= models.CASCADE, related_name='convites_recebidos')

    def aceitar(self):
        self.convidado.contatos.add(self.solicitante)
        self.solicitante.contatos.add(self.convidado)
        self.delete()

    def rejeitar(self):
        self.delete()
        
class Post(models.Model):
    titulo = models.CharField(max_length=250)
    text = models.TextField()
    data_postagem = models.DateTimeField(auto_now=True)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='posts')
    imagem = models.ImageField(null=True, blank=True, upload_to='uploads/postagem/')