from django.contrib import admin
from checklist.models import (Gravidade,)


@admin.register(Gravidade)
class Gravidadeadmin(admin.ModelAdmin):
    search_fields = ['categoria1','categoria2','valor','gravidade','acao','orientacao','acaocorretiva','ativo']
    list_display = ['categoria1','categoria2','valor','gravidade','acao','orientacao','acaocorretiva','ativo']
    #list_editable = ['categoria1','categoria2','valor','gravidade','acao','orientacao','acaocorretiva','ativo']
    #list_display_links = None