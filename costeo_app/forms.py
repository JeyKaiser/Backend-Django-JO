from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import  Collection


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = [
            'referencia',
            'foto_referencia',
            'codigo_sap_md',
            'codigo_sap_pt',
            'nombre_sistema',
            'descripcion_color',
            'codigo_color',
            'foto_tela',
            'nombre_referente',
            'linea',
            'creativo',
            'tecnico',
            'status',
            'tallaje',
            'largo',
            'modista',
        ]



# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'password1', 'password2')

#     # Sobrescribir la validación si es necesario
#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         if CustomUser.objects.filter(username=username).exists():
#             raise forms.ValidationError('Ya existe un usuario con este nombre de usuario.')
#         return username

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if CustomUser.objects.filter(email=email).exists():
#             raise forms.ValidationError('Ya existe una cuenta con este correo electrónico.')
#         return email

