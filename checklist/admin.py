from django.contrib import admin
from django.http import HttpResponse
import csv
from checklist.models import (Gravidade,)
from checklist.models import (Modelo,
                              Grupo,
                              Item,
                              ListaVerificacao,
                              )

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin, ExportCsvMixin):
    search_fields = ['nome','descricao']
    list_display = ['nome','descricao']
    actions = ["export_as_csv"]


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin, ExportCsvMixin):
    search_fields = ['nome','descricao']
    list_display = ['id','nome','descricao']
    #exclude = ['criadopor','criadoem','modificadopor','modificadoem']



@admin.register(Item)
class ItemAdmin(admin.ModelAdmin, ExportCsvMixin):
    search_fields = ['nome','descricao']
    list_display = ['id','nome','descricao','itemtipo','modelo_fk']


@admin.register(ListaVerificacao)
class ListaVerificacaoadmin(admin.ModelAdmin):
    search_fields = ['observacao','criadopor','modelo_fk','status']
    list_display = ['observacao','criadopor','modelo_fk','status']


@admin.register(Gravidade)
class Gravidadeadmin(admin.ModelAdmin):
    search_fields = ['categoria1','categoria2','valor','gravidade','acao','orientacao','acaocorretiva','ativo']
    list_display = ['categoria1','categoria2','valor','gravidade','acao','orientacao','acaocorretiva','ativo']
    #list_editable = ['categoria1','categoria2','valor','gravidade','acao','orientacao','acaocorretiva','ativo']
    #list_display_links = None



