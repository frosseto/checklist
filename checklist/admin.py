from django.contrib import admin
from django.http import HttpResponse
import csv
from checklist.models import (Acesso, Modelo,
                              Grupo,
                              Item,
                              ListaVerificacao,
                              ListaVerificacaoxItemxResposta,
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

    export_as_csv.short_description = "Exportar itens selecionados"


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

@admin.register(Acesso)
class AcessoAdmin(admin.ModelAdmin, ExportCsvMixin):
    search_fields = ['modelo_fk','usuario_fk','grupo_fk']
    list_display = ['modelo_fk','usuario_fk','grupo_fk']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin, ExportCsvMixin):
    search_fields = ['id','nome','descricao','itemtipo','modelo_fk','valorpadrao','valor_choice','grupo_fk','editavel']
    list_display = ['id','nome','descricao','itemtipo','modelo_fk','valorpadrao','valor_choice','grupo_fk','editavel']
    list_editable = ['nome','descricao','itemtipo','modelo_fk','valorpadrao','valor_choice','grupo_fk','editavel']


@admin.register(ListaVerificacao)
class ListaVerificacaoadmin(admin.ModelAdmin):
    search_fields = ['id','nome','observacao','criadopor','modelo_fk','status']
    list_display = ['id','nome','observacao','criadopor','modelo_fk','status']
    list_editable = ['nome','observacao','criadopor','modelo_fk','status']


#Remover as respostas do admin, na versão final
@admin.register(ListaVerificacaoxItemxResposta)
class ListaVerificacaoxItemxRespostaadmin(admin.ModelAdmin):
    search_fields = ['listaverificacao_fk','item_fk','resposta']
    list_display = ['id','listaverificacao_fk','item_fk','resposta']
    list_editable = ['listaverificacao_fk','item_fk','resposta']





