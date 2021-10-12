from checklist.filters import modeloFilter
from .models import (ListaVerificacao, 
                     ListaVerificacaoxItemxResposta,
                     Item,
                     Modelo,)
from rest_framework import serializers
from django.db import models


class listaverificacaoxitemxrespostaSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SerializerMethodField('id')
    listaverificacao_nome = serializers.CharField(source='listaverificacao_fk.modelo_fk.nome')
    item = serializers.CharField(source='item_fk.nome')
    itemtipo = serializers.CharField(source='item_fk.itemtipo')
    item_valorpadrao = serializers.CharField(source='item_fk.valorpadrao')
    class Meta:
        model = ListaVerificacaoxItemxResposta
        fields = ['id', 'listaverificacao_nome','item','itemtipo','item_valorpadrao','resposta']


class itemSerializer(serializers.HyperlinkedModelSerializer):
    modelo = serializers.IntegerField(source='modelo_fk.id')
    grupo = serializers.CharField(source='grupo_fk.nome')
    class Meta:
        model = Item
        fields = ['id', 'nome','descricao','modelo','grupo','itemtipo','valorpadrao']


class listaverificacaoSerializer(serializers.HyperlinkedModelSerializer):
    modelo = serializers.IntegerField(source='modelo_fk.pk')
    class Meta:
        model = ListaVerificacao
        fields = ['id','nome','modelo','observacao','status']

    def create(self, validated_data):
        modelo_fk=dict(validated_data.get('modelo_fk'))
        validated_data['modelo_fk']=None
        modelo = Modelo.objects.get(pk=modelo_fk['pk'])
        lv = ListaVerificacao(**validated_data)
        lv.modelo_fk=modelo
        lv.save()
        return lv


