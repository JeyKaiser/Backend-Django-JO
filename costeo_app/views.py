from rest_framework import generics,viewsets
from .models import Producto, Collection, Tela
from .serializers import ProductoSerializer, CollectionSerializer, TecnicoSerializer,TelaSerializer, CreativoSerializer
from .models import CustomUser, Status, Foto, Creativo, Tecnico, ColorReferencia, Tipo, Variacion, Collection, Sublinea, Linea, LineaSublinea
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm, CollectionForm
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        #print(request.POST)
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


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'miSignin': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'],
                    password=request.POST['password'])
        if user is None:            
            return render(request, 'signin.html',{
            'miSignin': AuthenticationForm,
            'error': 'Usuario o Contraseña es incorrecta'
        })
        else:
            login(request, user)
            return redirect('index')
        
    
def index(request):
    title = 'Django-Course!!'
    return render(request, "index.html")



def lista_Referencias(request):
    coleccion = Collection.objects.all()
    #print(coleccion.values())
    return render(request, 'colecciones/coleccion.html',{
        'miColeccion': coleccion,
    })


def create_reference(request):
    status = Status.objects.all()
    creativo = Creativo.objects.all()
    tecnico = Tecnico.objects.all()
    tipo = Tipo.objects.all()
    variacion = Variacion.objects.all()
    codigo_color = ColorReferencia.objects.all()
    linea = Linea.objects.all()
    sublinea = Sublinea.objects.all()
    color_ref = ColorReferencia.objects.all()

    if request.method == 'POST':
        form = CollectionForm(request.POST, request.FILES)
        print(
            request.POST.get('referencia'),
            request.POST.get('foto_referencia'),
            request.POST.get('nombre_sistema'),
            request.POST.get('codigo_sap_md'),
            request.POST.get('codigo_sap_pt'),
            request.POST.get('descripcion_color'),
            request.POST.get('creativo'),
            request.POST.get('tecnico'),
            request.POST.get('status'),
            request.POST.get('codigo_color'),
            request.POST.get('linea')
        )
        if form.is_valid():
            form.save()
            return redirect('collection')
    else:
        form = CollectionForm()

    return render(request, 'colecciones/create.html', {
        'form': form,
        'miCreativo': creativo,
        'miTecnico': tecnico,
        'miStatus': status,
        'miTipo': tipo,
        'miVariacion': variacion,
        'miColorReferencia': codigo_color,
        'miLinea': linea,
        'miSublinea': sublinea,
        'miDescripcionRef': color_ref,
        # 'miLineaSublinea': lineaSublinea,
    })

def RegisterReference(request):
    status = Status.objects.all()
    creativo = Creativo.objects.all()
    tecnico = Tecnico.objects.all()
    tipo = Tipo.objects.all()
    variacion = Variacion.objects.all()

    if request.method == "POST":
        referencia = request.POST.get('referencia')
        nombre_referente = request.POST.get('nombre_referente')
        codigo_sap_md = request.POST.get('codigo_sap_md')
        codigo_sap_pt = request.POST.get('codigo_sap_pt')
        status_id = request.POST.get('status')
        creativo_id = request.POST.get('creativo')
        tecnico_id = request.POST.get('tecnico')
        tipo_id = request.POST.get('tipo')
        variacion_id = request.POST.get('variacion')
        linea_id = request.POST.get('linea')

        print(referencia, nombre_referente, codigo_sap_md, codigo_sap_pt, status_id, creativo_id, tecnico_id, tipo_id, variacion_id, linea_id)

        foto_ref = request.FILES.get('foto')
        foto_referencia = None
        if foto_ref:
            fs = FileSystemStorage()
            filename = fs.save(foto_ref.name, foto_ref)
            uploaded_file_url = fs.url(filename)
            foto_referencia = Foto.objects.create(ruta_foto=uploaded_file_url)

        # Crear la nueva colección en la base de datos
        nueva_coleccion = Collection.objects.create(
            referencia=referencia,
            foto_referencia=foto_referencia,
            codigo_sap_md=codigo_sap_md,
            codigo_sap_pt=codigo_sap_pt,
            nombre_referente=nombre_referente,
            status_id=status_id,
            creativo_id=creativo_id,
            tecnico_id=tecnico_id,
            linea_id=linea_id,
        )
        return redirect('RegisterReference')

    return render(request, 'colecciones/register_ref.html', {
        'miStatus': status,
        'miCreativo': creativo,
        'miTecnico': tecnico,
        'miTipo': tipo,
        'miVariacion': variacion,
    })


def about(request):
    return render(request, "about.html")


def signout(request):
    logout(request)
    print('Salir de la sesión')
    return redirect('signin')



class ProductoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class CollectionCreateView(generics.CreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

class TecnicoViewSet(viewsets.ModelViewSet):
    queryset = Tecnico.objects.all()
    serializer_class = TecnicoSerializer

class TelaViewSet(viewsets.ModelViewSet):
    queryset = Tela.objects.all()
    serializer_class = TelaSerializer

class CreativoViewSet(viewsets.ModelViewSet):
    queryset = Creativo.objects.all()
    serializer_class = CreativoSerializer



@api_view(['GET'])
def lista_coleccion(request):
    nombre = request.GET.get('nombre')
    # Simulación básica
    data = [
        {'producto': 'Vestido largo', 'coleccion': nombre},
        {'producto': 'Chaqueta de cuero', 'coleccion': nombre},
    ]
    return Response(data)
