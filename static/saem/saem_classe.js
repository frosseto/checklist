/* Criacao de classe */
/* Modal para criar/editar classe */
var editClasse = function(){

    data_url = $(this).data('url')
    data_id = $(this).data('id')

    if(data_id != ''){
        data_url = data_url + data_id + '/'
    };
    console.log(data_url)

    $.ajax({
    url: data_url,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
        $('#create-update-modal').html(data.classe_modal);
        $('#create-update-modal').modal('show');
        $('.js-btn-classe-edit-acao').unbind('click');
        $('.js-btn-classe-edit-acao').click(acaoEditClasse);
        alerta(data);
    }
    });
}
/* Criar/editar classe */
var acaoEditClasse = function(){

    data_url = $(this).data('url')
    data_id = $(this).data('id')

    if(data_id != ''){
        data_url = data_url + data_id + '/'
    };
    console.log(data_url)

    form_classe = $('#form-create-edit-classe')
    classe_data = {
    'form-classe': form_classe.serialize(), 
    }
    console.log(form_classe)
    const csrftoken = getCookie('csrftoken');       
    $.ajax({
        url: data_url,
        data: classe_data,
        type: 'POST',
        dataType: 'json',
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (data) {
        $('#create-update-modal').modal('hide');
        alerta(data);
    }
    });
};

/* Selecao de classe herdada - operacao */

var listClasse = function(){
    var url=$(this).data('url');
    var page=$(this).data('page');
    var objeto_id = $('#objeto-denominacao').attr('objeto_pk')
    if(url=='/saem/classe-objeto-list'){
        objeto=objeto_id
    }
    else{
        objeto=''
    }
    carregaClasse(url,page,objeto)
}

var carregaClasse = function(url,page,objeto){
    var form_list_classe = $('#form-add-classe');
    console.log('url '+url+'; page '+page)
    $.ajax({
    url: url,
    type: 'get',
    data: form_list_classe.serialize()+'&page='+page+'&objeto='+objeto,
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
        $('#resultado-pesquisa-classe').html(data.resultado_pesquisa_classe)
        $('.js-btn-classe-list-filter').unbind('click');
        $('.js-btn-classe-list-filter').click(listClasse)   
        alerta(data);
        $('.js-btn-classe-edit-ltm-acao').unbind('click');
        $('.js-btn-classe-edit-ltm-acao').click(acaoSelectClasse); 
    }
    });
}

var acaoSelectClasse = function(){
    var id = $(this).data('id')
    var url = $(this).data('url')
    if(url == "/saem/classe/classe-herdada-select" || url == "/saem/classe/classe-herdada-remove/view/" || url == "/saem/classe/classe-herdada-remove/delete/"){
        acaoConfirmadaSelectClasse(id,url);
    }else if(url == "/saem/classe/objeto-remover-classe"){
        $("#titulo-confirmacao").text('Confirmação de remoção de Classe de Manutenção associada ao Objeto');
        $("#body-confirmacao").text('Confirma a remoção?');
        $("#modal-confirm").modal('show');
        $("#modal-confirm-btn").unbind("click");
        $("#modal-confirm-btn").bind("click",function(){
            acaoConfirmadaRemoverClasseObjeto(url);
        });
    
    }else{
        $("#titulo-confirmacao").text('Confirmação de alteração de classe');
        $("#body-confirmacao").text('Confirma a alteração?');
        $("#modal-confirm").modal('show');
        $("#modal-confirm-btn").unbind("click");
        $("#modal-confirm-btn").bind("click",function(){
            acaoConfirmadaSelectClasse(id,url);
        });
    }
}


/* Adicionar classe herdada */
var acaoConfirmadaSelectClasse = function(id,url){
    var classe_principal = $('#classe-denominacao').attr('classe_pk')
    var objeto_id = $('#objeto-denominacao').attr('objeto_pk')
    const csrftoken = getCookie('csrftoken'); 
    /* nao executar acao em modo de edicao - salvaguarda de edicao de operacao em andamento */
    if($("button[name='salvar'").is(":visible")){
        $("#save-ok-modal").modal('show');
        return;
    }

    $.ajax({
    url: url,
    data:  {'classe_principal': classe_principal, 
            'id': id,
            'objeto_id': objeto_id},
    type: 'POST',
    dataType: 'json',
    beforeSend: function(request) {
        request.setRequestHeader("X-CSRFToken", csrftoken);
        },
    success: function (data) {
        if(data.classe_modal != undefined){
            $('#create-update-ltm-modal').html(data.classe_modal);
            $('#create-update-ltm-modal').modal('show');
        }else if(data.classe_herdada_list != undefined){
            $('#classes-herdadas-list').html(data.classe_herdada_list) 
            $('#create-update-ltm-modal').modal('hide');
            loadData(tipo='classe',valor=classe_principal,url="/saem/ltm")
        }else{
            $('#create-update-ltm-modal').modal('hide');
            loadData(tipo='classe',valor=id,url="/saem/ltm")
        }
        setCtrl('')
        relink_ltm();
        alerta(data);
        $("#modal-confirm").modal('hide');
        }
    });
}

/* Modal para selecao de classe */
var selectClasse = function(url){
    console.log('selectClasse')
    var classe = $('#classe-denominacao').attr('classe_pk')

    $.ajax({
    url: url,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
        $('#create-update-ltm-modal').html(data.classe_modal);
        $('.js-btn-classe-list-filter').click(listClasse)
        $('#create-update-ltm-modal').modal('show');
        alerta(data);
        $('.js-btn-classe-edit-ltm-acao').unbind('click');
        $('.js-btn-classe-edit-ltm-acao').click(acaoSelectClasse);

        /* Verifica se Objeto já associado a classe e exibe botão */
        if(!!classe) {
            $('.js-btn-classe-edit-ltm-acao[name="objeto-remover-classe"]').show();
        }else{
            $('.js-btn-classe-edit-ltm-acao[name="objeto-remover-classe"]').hide();
        }
    }
    });
}

/* Remove associação de classe de manutenção em objeto  */
var acaoConfirmadaRemoverClasseObjeto = function(url){
    var objeto_id = $('#objeto-denominacao').attr('objeto_pk')    
    const csrftoken = getCookie('csrftoken'); 

    console.log('acaoConfirmadaRemoverClasseObjeto')
    console.log('Objeto: ' + objeto_id)

    $.ajax({
    url: url,
    data:  {'objeto_id': objeto_id},
    type: 'POST',
    dataType: 'json',
    beforeSend: function(request) {
        request.setRequestHeader("X-CSRFToken", csrftoken);
        },
    success: function (data) {
        $('#create-update-ltm-modal').modal('hide');
        loadData(tipo='objeto',valor=objeto_id,url="/saem/ltm")

        setCtrl('')
        relink_ltm();
        alerta(data);
        $("#modal-confirm").modal('hide');
        }
    });
}