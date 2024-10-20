from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Collection


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = [
            'referencia', 
            'fotoReferencia', 
            'nombreSistema', 
            'codigoSapMD', 
            'codigoSapPT',
            'codigoColor',                       
            'descripcionColor',                       
            'creativo',
            'tecnico',
            'status',
            'linea'
            #'sublinea',            
        ]



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    # Sobrescribir la validación si es necesario
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Ya existe un usuario con este nombre de usuario.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe una cuenta con este correo electrónico.')
        return email

