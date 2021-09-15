var carregaObjeto = function(url,page,objeto){
    var form_list_objeto = $('#form-add-objeto');
    console.log('url '+url+'; page '+page)
    $.ajax({
    url: url,
    type: 'get',
    data: form_list_objeto.serialize()+'&page='+page,
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
        $('#resultado-pesquisa-objeto').html(data.resultado_pesquisa_objeto)
        $('.js-btn-objeto-list-filter').unbind('click');
        $('.js-btn-objeto-list-filter').click(listObjeto)   
        alerta(data);
        $('.js-btn-objeto-edit-ltm-acao').unbind('click');
        $('.js-btn-objeto-edit-ltm-acao').click(acaoSelectObjeto); 
    }
    });
}


var listObjeto = function(){
    var url=$(this).data('url');
    var page=$(this).data('page');
    carregaObjeto(url,page)
}

var acaoSelectObjeto = function(){
    var id = $(this).data('id')
    var url = $(this).data('url')
    $("#titulo-confirmacao").text('Confirmação de alteração de objeto de referência');
    $("#body-confirmacao").text('Confirma a alteração?');
    $("#modal-confirm").modal('show');
    $("#modal-confirm-btn").unbind("click");
    $("#modal-confirm-btn").bind("click",function(){
        acaoConfirmadaSelectObjeto(id,url);
    });
}


/* Adicionar classe herdada */
var acaoConfirmadaSelectObjeto = function(id,url){
    var objeto_id = $('#objeto-denominacao').attr('objeto_pk')
    const csrftoken = getCookie('csrftoken'); 
    /* nao executar acao em modo de edicao - salvaguarda de edicao de operacao em andamento */
    if($("button[name='salvar'").is(":visible")){
        $("#save-ok-modal").modal('show');
        return;
    }

    $.ajax({
    url: url,
    data:  {'id': id,
            'objeto_id': objeto_id},
    type: 'POST',
    dataType: 'json',
    beforeSend: function(request) {
        request.setRequestHeader("X-CSRFToken", csrftoken);
        },
    success: function (data) {
        setCtrl('')
        relink_ltm();
        alerta(data);
        console.log(data)
        $('#objeto-referencia').html(data.objeto_referencia)
        $("#modal-confirm").modal('hide');
        $('#create-update-ltm-modal').modal('hide');
        
        }
    });
}


/* Modal para selecao de classe */
var selectObjetoReferencia = function(url){
    console.log('selectClasse')
    $.ajax({
    url: url,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
        $('#create-update-ltm-modal').html(data.classe_modal);
        $('.js-btn-objeto-list-filter').click(listObjeto)
        $('#create-update-ltm-modal').modal('show');
        alerta(data);
        $('.js-btn-objeto-edit-ltm-acao').unbind('click');
        $('.js-btn-objeto-edit-ltm-acao').click(acaoSelectObjeto);
    }
    });
}