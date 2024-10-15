#desde este archivo puedo añadir los modelos dentro del panel del administrador cuando ejecuto (python manage.py createsuperuser)
from django.contrib import admin
from.models import CustomUser, Collection, Tela, Linea, Status, Creativo, Tecnico, Foto, Tipo


#version corta
# admin.site.register(Aparrel)

admin.site.register(Collection)
admin.site.register(Tela)
admin.site.register(Linea)
admin.site.register(Status)
admin.site.register(Creativo)
admin.site.register(Tecnico)
admin.site.register(Foto)
admin.site.register(Tipo)


#admin.site.register(Task)

#admin.site.register(CustomUser)

