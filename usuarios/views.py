# from .models import Producto, Collection, Tela, CustomUser, Status
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.db import transaction
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SigninForm


def daniel(request):
    return render(request, 'daniel.html', {
        'miDaniel': AuthenticationForm
    })

def danielresponde(request):
    context = {
        'respuesta': 'Hola, soy Daniel, ¿en qué puedo ayudarte?',
        "nombre": 'Daniel',
        "apellido": 'Gonzalez',
    }
    return JsonResponse(context, status=200, safe=False)



#CREAR USUARIO NUEVO
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        # print(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            try:
                with transaction.atomic():
                    user = CustomUser.objects.create_user(
                        username=request.POST['username'],
                        password=request.POST['password1'],
                        email=request.POST['email']  # Agregar el email
                    )
                user.save()                # Iniciar sesión automáticamente después del registro
                login(request, user)
                messages.success(request, 'Cuenta creada con éxito.')
                print('Cuenta creada con éxito.')
                return redirect('signin')
            except Exception as e:
                print(f'Error: {e}')
                return render(request, 'signup.html', {'miSignup': form})
        else:
            messages.error(request, 'Las contraseñas no coinciden.')
            print('Las claves no son iguales.')
            return render(request, 'signup.html', {'miSignup': form})
    else:
        form = CustomUserCreationForm(request.POST)
        return render(request, 'signup.html', {'miSignup': form})


# Login de usuario
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'miSignin': SigninForm()
        })
    else:
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Aquí sí se llama a la función login con el usuario autenticado
                login(request, user)                
                return redirect('index')
            else:
                return render(request, 'signin.html', {
                    'miSignin': form,
                    'error': 'Usuario o Contraseña incorrecta'
                })
        else:
            return render(request, 'signin.html', {
                'miSignin': form,
                'error': 'Formulario inválido'
            })

