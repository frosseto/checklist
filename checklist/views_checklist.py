import json
from datetime import datetime

import plotly.graph_objects as go
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import connection
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
# from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from notifications.models import Notification
from notifications.signals import notify
from plotly.offline import plot
from django.contrib.contenttypes.models import ContentType

from checklist.settings import (PERFIL_APROVADOR, PERFIL_CONSULTA,
                                PERFIL_EXECUTANTE, PERFIL_MODELADOR)

from .filters import listaverificacaoFilter, modeloFilter
from .models import (Item, ListaVerificacao, ListaVerificacaoxItemxResposta,
                     Modelo)


# pesquisar lvs para visualizacao e edicao
@login_required(login_url='/accounts/login/')
def checklist_pesquisa(request):
    data = request.GET.copy()
    user = User.objects.get(username=request.user)
    filtered_qs = listaverificacaoFilter( 
                data, 
                ListaVerificacao.objects.all().order_by('-modificadoem','-criadoem')
            ).qs
    page = request.GET.get('page', 1)
    print(request.GET)
    listaverificacao_filter = listaverificacaoFilter(request.GET, queryset=filtered_qs)
    paginator = Paginator(filtered_qs, 40)
    
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
 
    args = {
        'filter': listaverificacao_filter, 
        'page_obj':response, 
        'notifications': user.notifications.unread()
        }
    return render(
        request, 
        'checklist_pesquisa_lv_preenchida.html', 
        args
    )


# pesquisar lvs para criacao
@login_required(login_url='/accounts/login/')
def checklist_nova_selecao(request):
    data = request.GET.copy()
    user = User.objects.get(username=request.user)
    filtered_qs = modeloFilter( 
                data, 
                Modelo.objects.all()
            ).qs
    
    page = request.GET.get('page', 1)
    print(request.GET)
    modelo_filter = modeloFilter(request.GET, queryset=filtered_qs)
    paginator = Paginator(filtered_qs, 40)
    
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
 
    args = {
        'filter': modelo_filter, 
        'page_obj':response, 
        'notifications': user.notifications.unread()
        }
    return render(
        request, 
        'checklist_pesquisa_nova.html', 
        args
    )


# criar e salvar lv
@login_required(login_url='/accounts/login/')
def checklist_nova(request,pk):
    if request.method == 'POST':

        data = request.POST 
        lv = json.loads(data.get('lv'))   
        lv_selected_itens = json.loads(data.get('lv_selected_itens'))  

        modelo=Modelo.objects.get(pk=lv['modelo'])

        listaverificacao=ListaVerificacao.objects.create(modelo_fk=modelo,
                                                         nome=lv['nome'],
                                                         observacao=lv['observacao'],
                                                         status=lv['status'],
                                                         criadopor = request.user,
                                                         criadoem=datetime.now())
        listaverificacao.save()

        print(lv_selected_itens)
        for key in lv_selected_itens:
            item=Item.objects.get(pk=key)
            item=ListaVerificacaoxItemxResposta.objects.create(listaverificacao_fk=listaverificacao,
                                                               item_fk=item,
                                                               resposta=lv_selected_itens[key])
            item.save()

        res={}
        res['msg'] = 'Sucesso'
        res['lv_pk'] = listaverificacao.id
        return JsonResponse(res)
    else:
        user = User.objects.get(username=request.user)
        context = {
            'modelo_pk': pk, 
            'lv_pk': '', 
            'acao': 'create', 
            'notifications': user.notifications.unread()
            }
        return render(request, 'checklist_form.html', context)
    

    
# visualizar e editar lv
@login_required(login_url='/accounts/login/')
def checklist(request,pk):
    user = User.objects.get(username=request.user)
    listaverificacao = ListaVerificacao.objects.get(pk=pk)
    modelo_pk = listaverificacao.modelo_fk.pk
    lv_pk = pk
    l=[]
    if user.has_perm(PERFIL_APROVADOR,listaverificacao.modelo_fk):
        l.append('Aprovador')
    if user.has_perm(PERFIL_EXECUTANTE,listaverificacao.modelo_fk):
        l.append('Executante')

    #l = user.groups.all().first()
    #print(list(request.user.groups.all().values_list('name', flat=True)))
    # for g in request.user.groups.all():
    #     l.append(g.name)
    
    if l:
        grupo_acesso = l
    else:
        grupo_acesso = ''
    
    context = {
        'modelo_pk': modelo_pk, 
        'lv_pk': lv_pk, 
        'acao': 'view',
        'notifications': user.notifications.unread(),
        'grupo_acesso': grupo_acesso
        }
    return render(request, 'checklist_form.html', context)




@login_required(login_url='/accounts/login/')
def checklist_delete(request,pk):
    ListaVerificacao.objects.get(pk=pk).delete()
    # notifications = Notification.objects.filter(notificationcta__cta_link=pk)
    # for n in notifications:
    #     n.delete()
    res={}
    res['msg'] = 'Sucesso'
    return JsonResponse(res)


@login_required(login_url='/accounts/login/')
def checklist_save(request,pk):
    if request.method == 'POST':
        data = request.POST 
        lv = json.loads(data.get('lv'))   
        lv_selected_itens = json.loads(data.get('lv_selected_itens'))  

        user = User.objects.get(username=request.user)
        listaverificacao = ListaVerificacao.objects.get(pk=pk)
        l=[]
        if user.has_perm(PERFIL_APROVADOR,listaverificacao.modelo_fk):
            l.append('Aprovador')
        if user.has_perm(PERFIL_EXECUTANTE,listaverificacao.modelo_fk):
            l.append('Executante')
        #l = user.groups.all().first()
        # l=[]
        # for g in request.user.groups.all():
        #     l.append(g.name)
        if l:
            grupo_acesso = l
        else:
            grupo_acesso = ''

        print(grupo_acesso, lv['status'])

        sender = User.objects.get(username=request.user)
        # listaverificacao = ListaVerificacao.objects.get(pk=lv['id'])
        print(grupo_acesso)
        if 'Aprovador' in grupo_acesso and lv['status']=='Aprovada':
            Notification.objects.filter(target_object_id=lv['id'],target_content_type=ContentType.objects.get_for_model(ListaVerificacao)).delete()
            
        elif 'Aprovador' in grupo_acesso and lv['status']=='Em elaboração':
            Notification.objects.filter(target_object_id=lv['id'],target_content_type=ContentType.objects.get_for_model(ListaVerificacao)).delete()
            
            receiver = User.objects.get(username=listaverificacao.modificadopor if listaverificacao.modificadopor != '' else listaverificacao.criadopor)
            notify.send(sender, 
                        recipient=receiver, 
                        verb='LV devolvida', 
                        description=f"LV {lv['id']} devolvida pelo aprovador",
                        target=listaverificacao) #lv['id']
        elif 'Executante' in grupo_acesso and lv['status']=='Aguardando Aprovador':
            Notification.objects.filter(target_object_id=lv['id'],target_content_type=ContentType.objects.get_for_model(ListaVerificacao)).delete()
            users = User.objects.filter(groups__name='Aprovador')
            # grupo=Group.objects.filter(name='Aprovador')
            for user in users:
                notify.send(sender, 
                            recipient=user, 
                            verb='LV enviada para aprovação', 
                            description=f"LV {lv['id']} aguardando aprovador",
                            target=listaverificacao
                            )
        else:
            pass
    
        listaverificacao.nome = lv['nome']
        listaverificacao.observacao = lv['observacao']
        listaverificacao.status=lv['status']
        listaverificacao.modificadopor = request.user
        listaverificacao.modificadoem = datetime.now()
        listaverificacao.save()

        print(lv_selected_itens)
        for key in lv_selected_itens:
            item = Item.objects.get(pk=key)
            itemresposta = ListaVerificacaoxItemxResposta.objects.filter(listaverificacao_fk=listaverificacao,item_fk=item)
            if itemresposta:
                print('update',key,str(lv_selected_itens[key]))
                itemresposta.update(
                    resposta = str(lv_selected_itens[key])
                )
            else:
                print('create',key,str(lv_selected_itens[key]))
                ListaVerificacaoxItemxResposta.objects.create(listaverificacao_fk=listaverificacao,
                                                              item_fk=item,
                                                              resposta=str(lv_selected_itens[key]))
 
        res={}
        res['msg'] = 'Sucesso'
        return JsonResponse(res)



from . import relatorio_dash_app


@login_required(login_url='/accounts/login/')
def checklist_relatorio(request):
	def scatter():
		x1 = [1,2,3,4,5,6,7,8]
		y1 = [38, 35, 25, 45]

		trace = go.Scatter(
			x = x1,
			y = y1
		)
		layout = dict(
			title = 'Relatório',
			xaxis = dict(range=[min(x1),max(x1)]),
			yaxis = dict(range=[min(y1),max(y1)])
		)
		fig = go.Figure(data=[trace], layout=layout)
		plot_div = plot(fig, output_type='div', include_plotlyjs=False)
		return plot_div

	context = {
		'plot': scatter()
	}
	return render(request, 'checklist_relatorio.html', context)



