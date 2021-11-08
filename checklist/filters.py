import django_filters
from django_filters import DateRangeFilter, DateFilter, BooleanFilter
from django import forms
from django.db import models
from .models import (Modelo,
                     ListaVerificacao)
from guardian.shortcuts import get_objects_for_user
from .settings import (PERFIL_APROVADOR, PERFIL_CONSULTA, PERFIL_EXECUTANTE,
                       PERFIL_MODELADOR)

                   
class modeloFilter(django_filters.FilterSet):
    class Meta:
        model = Modelo
        fields = ['nome', 'descricao']
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }


# def queryset_modelos(user):
#     if user:
#         objetosPermitidos=get_objects_for_user(user,[PERFIL_APROVADOR,PERFIL_EXECUTANTE,PERFIL_CONSULTA],Modelo,any_perm=True)
#         return Modelo.objects.filter(pk__in =objetosPermitidos)
#     else:
#         return Modelo.objects.filter(pk__in =[2])
        



class listaverificacaoFilter(django_filters.FilterSet):
    modelos = None
    def __init__(self, *args, **kwargs):
        if 'modelos' in kwargs:
            modelo = kwargs.pop('modelos')
            print(modelo)
        super(listaverificacaoFilter, self).__init__(*args, **kwargs)

    # modelo_fk=django_filters.ModelChoiceFilter(
    # queryset=queryset_modelos(user)
# )

    class Meta:
        model = ListaVerificacao
        fields = ['observacao','criadopor','modelo_fk','status']
    filter_overrides = {
        models.CharField: {
            'filter_class': django_filters.CharFilter,
            'extra': lambda f: {
                'lookup_expr': 'icontains',
            },
        },
    }

    

