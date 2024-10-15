from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser




class CreateNewReference(forms.Form):
    referencia  =    forms.CharField(label="Nombre de tarea", max_length=30, widget=forms.TextInput(attrs={'class':'input'}))    
    fotoreferencia = forms.CharField(label="Nombre de tarea", max_length=30, widget=forms.TextInput(attrs={'class':'input'}))
    codigoSapMD =    forms.CharField(label="Nombre de tarea", max_length=30, widget=forms.TextInput(attrs={'class':'input'}))    
    codigoSaoPT =    forms.CharField(label="Nombre de tarea", max_length=30, widget=forms.TextInput(attrs={'class':'input'}))
    nombreSistema =  forms.CharField(label="Nombre de tarea", max_length=30, widget=forms.TextInput(attrs={'class':'input'}))    
    descripcionColor=forms.CharField(label="Nombre de tarea", max_length=200, widget=forms.TextInput(attrs={'class':'input'}))
    codigoColor =    forms.CharField(label="Nombre de tarea", max_length=200, widget=forms.TextInput(attrs={'class':'input'}))    
    fotoTela =       forms.CharField(label="Nombre de tarea", max_length=30, widget=forms.TextInput(attrs={'class':'input'}))
    nombreReferente =forms.CharField(label="Nombre de tarea", max_length=20, widget=forms.TextInput(attrs={'class':'input'}))    
    linea =          forms.CharField(label="Nombre de tarea", max_length=30, widget=forms.TextInput(attrs={'class':'input'}))
    creativo =       forms.CharField(label="Nombre de tarea", max_length=30, widget=forms.TextInput(attrs={'class':'input'}))    
    tecnico =        forms.CharField(label="Nombre de tarea", max_length=30, widget=forms.TextInput(attrs={'class':'input'}))
    status =         forms.CharField(label="Nombre de tarea", max_length=30, widget=forms.TextInput(attrs={'class':'input'}))    
    tallaje =        forms.CharField(label="Nombre de tarea", max_length=50, widget=forms.TextInput(attrs={'class':'input'}))
    largo =          forms.CharField(label="Nombre de tarea", max_length=50, widget=forms.TextInput(attrs={'class':'input'}))    
    modista =        forms.CharField(label="Nombre de tarea", max_length=100, widget=forms.TextInput(attrs={'class':'input'}))   


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

