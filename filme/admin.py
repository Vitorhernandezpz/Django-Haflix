from django.contrib import admin
from .models import Filme, Episodeo, Usuario
from django.contrib.auth.admin import UserAdmin

# só existe porque queremos que no admin apareça o campo personalizado filmes-vistos
campos = list(UserAdmin.fieldsets)
campos.append(
    ("Histórico",{'fields': ('filmes_vistos',)})
)
UserAdmin.fieldsets = tuple(campos)

# Register your models here.
admin.site.register(Filme)
admin.site.register(Episodeo)
admin.site.register(Usuario, UserAdmin)