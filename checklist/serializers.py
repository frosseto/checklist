from checklist.filters import modeloFilter
from .models import (ListaVerificacao, 
                     ListaVerificacaoxItemxResposta,
                     Item,
                     Modelo,)
from rest_framework import serializers
from django.db import models


class listaverificacaoxitemxrespostaSerializer(serializers.HyperlinkedModelSerializer):

    listaverificacao = serializers.IntegerField(source='listaverificacao_fk.id')
    item = serializers.IntegerField(source='item_fk.id')
    class Meta:
        model = ListaVerificacaoxItemxResposta
        fields = ['id','listaverificacao','item','resposta']

    # def create(self, validated_data):
    #     print(validated_data)
    #     item_fk=dict(validated_data.get('item_fk'))
    #     listaverificacao_fk=dict(validated_data.get('listaverificacao_fk'))
    #     validated_data['item_fk']=None
    #     validated_data['listaverificacao_fk']=None
    #     listaverificacao = ListaVerificacao.objects.get(pk=listaverificacao_fk['id'])
    #     item = Item.objects.get(pk=item_fk['id'])
    #     lv_resposta = ListaVerificacaoxItemxResposta(**validated_data)
    #     lv_resposta.listaverificacao_fk=listaverificacao
    #     lv_resposta.item_fk=item
    #     lv_resposta.save()
    #     return lv_resposta

    


class itemSerializer(serializers.HyperlinkedModelSerializer):
    modelo = serializers.IntegerField(source='modelo_fk.id')
    grupo = serializers.CharField(source='grupo_fk.nome')
    class Meta:
        model = Item
        fields = ['id', 'nome','descricao','modelo','grupo','itemtipo','valorpadrao']


class modeloSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Modelo
        fields = ['id', 'nome','descricao']
        


class listaverificacaoSerializer(serializers.HyperlinkedModelSerializer):
    modelo = serializers.IntegerField(source='modelo_fk.id')
    class Meta:
        model = ListaVerificacao
        fields = ['id','nome','modelo','observacao','status']

    def create(self, validated_data):
        print(validated_data)
        modelo_fk=dict(validated_data.get('modelo_fk'))
        validated_data['modelo_fk']=None
        modelo = Modelo.objects.get(pk=modelo_fk['id'])
        lv = ListaVerificacao(**validated_data)
        lv.modelo_fk=modelo
        lv.save()
        return lv




