from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (Item, ListaVerificacaoxItemxResposta, OrdemPesquisa, 
                     SAO, 
                     SAOResultado,
                     Modelo,
                     ListaVerificacao)
from .filters import (ordemFilter, 
                      modeloFilter,
                      listaverificacaoFilter,)
from .forms import SAOForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.db import connection
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from plotly.offline import plot
import plotly.graph_objects as go
import json


anp = {'na': 'NA',
        'detector-fogo':'Fogo',
        'detector-gas':'Gas',
        'bdv':'BDV',
        'adv':'ADV',
        'adv-teste-seco': 'ADV - Teste Seco',
        'adv-teste-molhado': 'ADV - Teste Molhado',
        'sdv':'SDV',
        'partida-ub':'Partida UB'}

anp_legado = {'NA': 'na',
              'UB': 'partida-ub',
              'SDV': 'sdv',
              'Gas': 'detector-gas',
              'ADV': 'adv',
              'Fogo': 'detector-fogo',
              'BDV': 'detector-gas'}


# pesquisar lvs para visualizacao e edicao
@login_required(login_url='/accounts/login/')
def checklist_pesquisa(request):
    data = request.GET.copy()
    filtered_qs = listaverificacaoFilter( 
                data, 
                ListaVerificacao.objects.all()
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
 
    args = {'filter': listaverificacao_filter, 'page_obj':response}
    return render(
        request, 
        'checklist_pesquisa_lv_preenchida.html', 
        args
    )


# pesquisar lvs para criacao
@login_required(login_url='/accounts/login/')
def checklist_nova_selecao(request):
    data = request.GET.copy()
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
 
    args = {'filter': modelo_filter, 'page_obj':response}
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
                                                         status=lv['status'])
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
        context = {'modelo_pk': pk, 'lv_pk': '', 'acao': 'create'}
        return render(request, 'checklist_form.html', context)
    

    
# visualizar e editar lv
@login_required(login_url='/accounts/login/')
def checklist(request,pk):
    listaverificacao = ListaVerificacao.objects.get(pk=pk)
    modelo_pk = listaverificacao.modelo_fk.pk
    lv_pk = pk
    context = {'modelo_pk': modelo_pk, 'lv_pk': lv_pk, 'acao': 'view'}
    return render(request, 'checklist_form.html', context)




@login_required(login_url='/accounts/login/')
def checklist_delete(request,pk):
    if request.method == 'POST':
        data = request.POST 
        print(data)
        res={}
        res['msg'] = 'Sucesso'
        return JsonResponse(res)


@login_required(login_url='/accounts/login/')
def checklist_save(request,pk):
    if request.method == 'POST':

        data = request.POST 
        lv = json.loads(data.get('lv'))   
        lv_selected_itens = json.loads(data.get('lv_selected_itens'))  

        listaverificacao = ListaVerificacao.objects.get(pk=lv['id'])
        listaverificacao.nome = lv['nome']
        listaverificacao.observacao = lv['observacao']
        listaverificacao.save()

        for key in lv_selected_itens:
            print(key,lv_selected_itens[key])
            item = Item.objects.get(pk=key)
            itemresposta = ListaVerificacaoxItemxResposta.objects.filter(listaverificacao_fk=listaverificacao,item_fk=item)
            if itemresposta:
                itemresposta.resposta = str(lv_selected_itens[key])
            else:
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



