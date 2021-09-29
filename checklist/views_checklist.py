from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (OrdemPesquisa, 
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

@login_required(login_url='/accounts/login/')
def checklist_nova(request,pk):
    return render(request, 'checklist_form.html')


@login_required(login_url='/accounts/login/')
def checklist(request,pk):
    return render(request, 'checklist_form.html')


@login_required(login_url='/accounts/login/')
def checklist_edit(request,pk):
    return render(request, 'checklist_form.html')

@login_required(login_url='/accounts/login/')
def checklist_save(request,pk):
    return render(request, 'checklist_form.html')

@login_required(login_url='/accounts/login/')
def checklist_edit_cancel(request,pk):
    return render(request, 'checklist_form.html')

# Create your views here.
@login_required(login_url='/accounts/login/')
def sao_inicio(request):

    # valores iniciais
    data = request.GET.copy()
    if len(data) == 0:
        data['date_range'] = 'month'
    else:
        data = request.GET
    filtered_qs = ordemFilter( 
                data, 
                OrdemPesquisa.objects.all()
            ).qs
    
    page = request.GET.get('page', 1)
    print(request.GET)
    ordem_filter = ordemFilter(request.GET, queryset=filtered_qs)
    paginator = Paginator(filtered_qs, 40)
    
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    args = {'filter': ordem_filter, 'page_obj':response}
    return render(
        request, 
        'sao.html', 
        args
    )

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



@login_required(login_url='/accounts/login/')
def sao_ordem(request, ordem):
    print('here we go',ordem)
    data = dict()
    query_lv = f"""SELECT grav.tblGravidadeID, Categoria1, Valor, Orientacao, CASE WHEN res.tblGravidadeID IS NOT NULL THEN 1 ELSE 0 END Sel 
                    FROM dbsao.tblGravidade grav
                    LEFT JOIN (SELECT * FROM dbsao.tblResultado WHERE Ordem = '{ordem}') res
                    ON grav.tblGravidadeID = res.tblGravidadeID
                    WHERE grav.Ativo = 1"""
    plan = SAOResultado.objects.raw(query_lv + "AND Categoria1 = 'Planejamento de atividade' ORDER BY Categoria1 DESC")
    cont = SAOResultado.objects.raw(query_lv + "AND Categoria1 = 'Controle' ORDER BY Categoria1 DESC")
    exec = SAOResultado.objects.raw(query_lv + "AND Categoria1 = 'Execução' ORDER BY Categoria1 DESC")
    ence = SAOResultado.objects.raw(query_lv + "AND Categoria1 = 'Encerramento' ORDER BY Categoria1 DESC")

    auditoria_ordem = get_object_or_404(SAO, ordem=ordem)
    form = SAOForm(instance=auditoria_ordem)

    query_anp = f"SELECT TipoEquipamento, Teste, Falha FROM [DB6FA3].[dbsao].[tblANP]  WHERE Ordem = '{ordem}'"
    equipamento = 'na'
    n_testes_val = '0'
    n_falhas_val = '0'
    grupo_roteiro = None
    numerador = None
    with connection.cursor() as cursor:
        cursor.execute(query_anp)
        row = cursor.fetchone()
        if row:
            equipamento,n_testes_val,n_falhas_val = row
            if equipamento in anp_legado.keys():
                equipamento = anp_legado[equipamento]
        grupo_roteiro = cursor.execute(f"SELECT GrpRoteiro FROM [DB6FA3].[dbsao].[iw39] WHERE Ordem = {ordem}").fetchone()
        numerador = cursor.execute(f"SELECT NumGrp FROM [DB6FA3].[dbsao].[iw39] WHERE Ordem = {ordem}").fetchone()
    data['equipamento']=anp[equipamento]
    data['n_testes_val']=n_testes_val
    data['n_falhas_val']=n_falhas_val
    if grupo_roteiro:
        data['grupo_roteiro']=grupo_roteiro[0]
    if numerador:
        data['numerador']=numerador[0]
    context = {'auditoria_ordem':auditoria_ordem,'form': form, 'plan': plan,'cont': cont, 'exec': exec, 'ence':ence,'data': data}
    return render(request, 'sao_ordem.html', context)
    #return save_uep_form(request, form, '_uep_update.html', uep)

@csrf_protect
def sao_ordem_save(request,ordem):
    data = dict()
    auditoria_ordem = get_object_or_404(SAO, ordem=ordem)
    print(auditoria_ordem.ordem)
    if request.method == 'POST':
        form_data = request.POST 
        auditoria_ordem.observacaoanalista = form_data.get('observacaoanalista')
        auditoria_ordem.observacaolocal = form_data.get('observacaolocal')
        auditoria_ordem.executadopor = form_data.get('executadopor')
        auditoria_ordem.encerradotecnicamentepor = form_data.get('encerradotecnicamentepor')
        auditoria_ordem.confirmadopor = form_data.get('confirmadopor')
        resultado = 'Em análise'
        with connection.cursor() as cursor:
            cursor.execute(f"""DELETE FROM dbsao.tblResultado WHERE Ordem = {ordem};
                               DELETE FROM dbsao.tblANP WHERE Ordem = {ordem};""")
            equipamento = 'na'
            n_testes_val = 0
            n_falhas_val = 0
            for key in form_data:
                if "lv_" in key:
                    #print(key,form_data[key])
                    item_lv_num = key.split("_")[1]
                    query_item_lv = f"INSERT INTO dbsao.tblResultado (Ordem,tblGravidadeID) VALUES ('{ordem}','{item_lv_num}')"
                    cursor.execute(query_item_lv)
                elif key == "equipamento":
                    equipamento = form_data[key]
                elif key == "n_testes_val":
                    n_testes_val = form_data[key] or 0
                elif key == "n_falhas_val":
                    n_falhas_val = form_data[key] or 0
            print(equipamento,n_testes_val,n_falhas_val)
            if equipamento != 'na':
                with connection.cursor() as cursor:
                    cursor.execute(f"""INSERT INTO dbsao.tblANP (Ordem, TipoEquipamento, Teste, Falha) VALUES 
                                    ({ordem},'{equipamento}',{n_testes_val},{n_falhas_val});""")    
        #recalcular resultado
        with connection.cursor() as cursor:
            resultado=cursor.execute(f"""
                                    SELECT
                                    CASE WHEN Gravidade<>'Conforme' THEN tblNivelGravidade.Gravidade
                                            WHEN tblNivelGravidade.Gravidade='Conforme' AND  res.AnalisadoPor IS NULL THEN 'Em análise'
                                            ELSE 'Conforme'
                                            END
                                    FROM
                                    (
                                    SELECT a.Ordem, MAX(a.Nivel) 
                                    Nivel FROM (SELECT Ordem, tblNivelGravidade.Nivel 
                                    FROM [DB6FA3].[dbsao].[tblResultado] 
                                    LEFT JOIN dbsao.tblGravidade 
                                    ON [tblResultado].tblGravidadeID = tblGravidade.tblGravidadeID 
                                    LEFT JOIN dbsao.tblNivelGravidade 
                                    ON [tblGravidade].Gravidade = tblNivelGravidade.Gravidade) a 
                                    GROUP BY a.Ordem
                                    ) b 
                                    LEFT JOIN dbsao.tblNivelGravidade 
                                    ON dbsao.tblNivelGravidade.Nivel = b.Nivel 
                                    LEFT JOIN dbsao.tblSAO res
                                    ON b.Ordem = res.Ordem
                                    WHERE res.Ordem = {ordem}
                                    """).fetchone()[0]

    data = dict()
    data['titulo'] = 'Salvar'
    data['msg'] = f"Dados salvos - Gravidade identificada: {resultado}"
    data['resultado'] = resultado

    usuario = str(request.user)
    auditoria_ordem.analisadopor = usuario + '|Libe'
    status_str = 'Ordem analisada'
    auditoria_ordem.dataanalise = timezone.localtime(timezone.now())
    auditoria_ordem.status = status_str
    auditoria_ordem.resultado=resultado
    data['status'] = status_str

    auditoria_ordem.save()
    return JsonResponse(data)


def sao_ordem_edit(request, ordem):
    data = dict()
    auditoria_ordem = get_object_or_404(SAO, ordem=ordem)
    analisado_por = getattr(auditoria_ordem,'analisadopor')
    status_str = getattr(auditoria_ordem,'status')
    data['titulo'] = 'Edição'
    data['msg'] = 'Checkout realizado com sucesso'
    data['estado_edicao'] = 'Libe'
    data['status'] = status_str

    usuario = str(request.user)
    analisado_por = analisado_por or '|Libe'
    tmp = analisado_por.split("|")
    data['analista'] = tmp[0] or usuario
    data['estado_edicao'] = tmp[1] 

    if data['estado_edicao'] == 'Lock' and data['analista'] != usuario:
        data['msg'] = f"A lista etá travada com o analista {data['analista']}"
    else:
        auditoria_ordem.analisadopor = usuario + '|Lock'
        status_str = 'Em análise pelo EPIM'
        #auditoria_ordem.status = status_str
        data['status'] = status_str
        data['estado_edicao'] = 'Libe'
        data['analista'] = usuario 
        auditoria_ordem.save()
    print(status_str)
    print('sao_ordem_edit',analisado_por, usuario)
    return JsonResponse(data)


def sao_ordem_cancel(request, ordem):
    usuario = str(request.user)
    data = dict()
    if ordem:
        auditoria_ordem = get_object_or_404(SAO, ordem=ordem)
        auditoria_ordem.analisadopor = usuario + '|Libe'
        auditoria_ordem.save()
        return HttpResponseRedirect('/sao/ordem/%s' % ordem)
    else:
        return HttpResponseRedirect('/sao/')


def sao_proxima_ordem(request):
    print('sao_proxima_ordem')
    ordem = None
    with connection.cursor() as cursor:
        cursor.execute('EXEC [dbsao].[ProximaOrdem]')
        row = cursor.fetchall()
        if row:
            ordem = row[0]
    if ordem:
        return HttpResponseRedirect('/sao/ordem/%s' % ordem)
    else:
        return HttpResponseRedirect('/sao/ordem/')