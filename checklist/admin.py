from django.contrib import admin
from django.http import HttpResponse
import csv
from django.contrib import messages
from checklist.models import (Acesso, Modelo,
                              Grupo,
                              Item,
                              ListaVerificacao,
                              ListaVerificacaoxItemxResposta,
                              )
from guardian.models import *

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

# @admin.register(GroupObjectPermission)
# class GroupObjectPermissionAdmin (admin.ModelAdmin, ExportCsvMixin):
#     list_display = [field.name for field in GroupObjectPermission._meta.get_fields()]

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin, ExportCsvMixin):
    search_fields = ['nome','descricao']
    list_display = ['id','nome','descricao']
    #exclude = ['criadopor','criadoem','modificadopor','modificadoem']

@admin.register(Acesso)
class AcessoAdmin(admin.ModelAdmin, ExportCsvMixin):
    search_fields = ['modelo_fk','perfil','grupo_fk']
    list_display = ['modelo_fk','perfil','grupo_fk']

    def save_model(self, request, obj, form, change):
        if not(obj.pk is None):
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Não é permitida alteração ... Caso necessite modificar algo, será necessário excluir esta regra e criar uma nova')
        else:
            super(AcessoAdmin, self).save_model(request, obj, form, change)
    
    def delete_queryset(self, request, queryset): #necessário para o admin'
        for obj in queryset:
            obj.delete()
    
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin, ExportCsvMixin):
    search_fields = ['id','nome','descricao','itemtipo','modelo_fk','valorpadrao','valor_choice','grupo_fk','editavel']
    list_display = ['id','nome','descricao','itemtipo','modelo_fk','valorpadrao','valor_choice','grupo_fk','editavel']
    list_editable = ['nome','descricao','itemtipo','modelo_fk','valorpadrao','valor_choice','grupo_fk','editavel']


# @admin.register(ListaVerificacao)
# class ListaVerificacaoadmin(admin.ModelAdmin):
#     search_fields = ['id','nome','observacao','criadopor','modelo_fk','status']
#     list_display = ['id','nome','observacao','criadopor','modelo_fk','status']
#     list_editable = ['nome','observacao','criadopor','modelo_fk','status']


#Remover as respostas do admin, na versão final
# @admin.register(ListaVerificacaoxItemxResposta)
# class ListaVerificacaoxItemxRespostaadmin(admin.ModelAdmin):
#     search_fields = ['listaverificacao_fk','item_fk','resposta']
#     list_display = ['id','listaverificacao_fk','item_fk','resposta']
#     list_editable = ['listaverificacao_fk','item_fk','resposta']





