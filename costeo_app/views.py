from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser, Status, Foto, Creativo, Tecnico, Linea, Tela, Tipo, Variacion, Collection
from .forms import CustomUserCreationForm, CollectionForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db import transaction
from django.core.files.storage import FileSystemStorage


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

# Crear una nueva referencia
def create_collection(request):
    status = Status.objects.all()
    creativo = Creativo.objects.all()
    tecnico = Tecnico.objects.all()
    tipo = Tipo.objects.all()
    variacion = Variacion.objects.all()
    print(creativo)

    if request.method == 'POST':
        form = CollectionForm(request.POST, request.FILES)
        print(request.POST.get('referencia'), request.POST.get('creativo'))    #ejemplo
        if form.is_valid():
            form.save()
            return redirect('create_collection')
    else:
        form = CollectionForm()
        
    return render(request, 'colecciones/create.html', {
        'form': form,
        'miCreativo': creativo,
        })

def RegisterReference(request):
    status = Status.objects.all()
    creativo = Creativo.objects.all() 
    tecnico = Tecnico.objects.all()
    tipo = Tipo.objects.all()
    variacion = Variacion.objects.all()

    if request.method == "POST":
        referencia  = request.POST.get('referencia')
        nombreRef   = request.POST.get('nombreRef')
        codigoSapMD = request.POST.get('codigoSapMD')
        codigoSapPT = request.POST.get('codigoSapPT')
        status_id   = request.POST.get('status')
        creativo_id = request.POST.get('creativo')
        tecnico_id  = request.POST.get('tecnico')
        tipo_id     = request.POST.get('tipo')
        variacion_id= request.POST.get('variacion')
        linea_id    = request.POST.get('linea')

        print(referencia, nombreRef, codigoSapMD, codigoSapPT, status_id, creativo_id, tecnico_id, tipo_id, variacion_id, linea_id)

        fotoRef = request.FILES.get('foto')
        foto_referencia = None
        if fotoRef:            
            fs = FileSystemStorage()
            filename = fs.save(fotoRef.name, fotoRef)
            uploaded_file_url = fs.url(filename)
            foto_referencia = Foto.objects.create(rutaFoto=uploaded_file_url)  
        
        # Crear la nueva colección en la base de datos
        nueva_coleccion = Collection.objects.create(
            referencia    = referencia,
            fotoReferencia= foto_referencia,
            codigoSapMD   = codigoSapMD,
            codigoSapPT   = codigoSapPT,
            nombreSistema = nombreRef,
            status_id     = status_id,
            creativo_id   = creativo_id,
            tecnico_id    = tecnico_id,
            linea_id      = linea_id,
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


