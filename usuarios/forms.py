from django import forms
from django.contrib.auth.models import User

class RegistrarUsuarioForm(forms.Form):
    nome = forms.CharField(required=True)
    email = forms.CharField(required=True)  # Definindo todos como obrigatorios
    senha = forms.CharField(required=True)
    telefone = forms.CharField(required=True)

    def is_valid(self):
        valid = True
        if not super(RegistrarUsuarioForm, self).is_valid():  # Se as informações não forem valida ("super" -> classe derivada referindo a classe base)
            self.adiciona_erro('Por favor verifique os campos informados.')
            valid = False

        user_exists = User.objects.filter(username=self.cleaned_data['email']).exists() # Verificar se o usuario existe
        if user_exists: # Caso ele exista, infoorma que já está cadastrado
            self.adiciona_erro('Usuário já cadastrado')
            valid = False

        return valid
    
    def adiciona_erro(self, message):
        errors = None  # Passando valor nulo
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())  #
        errors.append(message)