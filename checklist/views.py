from django.shortcuts import render
from django import template
from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404

#django rest
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from .serializers import (listaverificacaoxitemxrespostaSerializer, 
                          itemSerializer,
                          listaverificacaoSerializer,)
from .models import (ListaVerificacaoxItemxResposta,
                     Item,
                     ListaVerificacao,)


class listaverificacaoxitemxrespostaViewSet(viewsets.ModelViewSet):
    queryset = ListaVerificacaoxItemxResposta.objects.all()
    serializer_class = listaverificacaoxitemxrespostaSerializer
    permission_classes = [permissions.IsAuthenticated]


class itemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = itemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
            queryset = Item.objects.all()
            modelo = self.request.query_params.get('modelo')
            if modelo is not None:
                queryset = queryset.filter(modelo_fk__id=modelo)
            return queryset


class listaverificacacaoViewSet(viewsets.ModelViewSet):
    queryset = ListaVerificacao.objects.all()
    serializer_class = listaverificacaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None):
            queryset = ListaVerificacao.objects.all()
            lv = get_object_or_404(queryset, pk=pk)
            serializer = listaverificacaoSerializer(lv)
            return Response(serializer.data)

register = template.Library()
@register.filter(name='has_group')


def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

def index(request):
    return render(request, 'index.html', {})

