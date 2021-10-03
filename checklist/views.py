from django.shortcuts import render
from django import template
from django.contrib.auth.models import Group

#django rest
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import (listaverificacaoxitemxrespostaSerializer, 
                          itemSerializer)
from .models import (ListaVerificacaoxItemxResposta,
                     Item)


class listaverificacaoxitemxrespostaViewSet(viewsets.ModelViewSet):
    queryset = ListaVerificacaoxItemxResposta.objects.all()
    serializer_class = listaverificacaoxitemxrespostaSerializer
    permission_classes = [permissions.IsAuthenticated]


class itemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = itemSerializer
    permission_classes = [permissions.IsAuthenticated]


register = template.Library()
@register.filter(name='has_group')


def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

def index(request):
    return render(request, 'index.html', {})

