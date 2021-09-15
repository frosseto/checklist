/* Documentos associados com operação */
var acaoEditDocumentoLTM = function(){
    var operacao_id = $('#operacao-select').val();
    var objeto_id = $('#objeto-denominacao').attr('objeto_pk')
    var documento_id = $(this).data('id')

    form_documento = $('#form-update-remove-documento')
    console.log('acaoEditDocumentoLTM')
    const csrftoken = getCookie('csrftoken'); 
    $.ajax({
    url: $(this).data('url'),
    data:  {'operacao_id': operacao_id, 
            'documento_id': documento_id,
            'objeto_id': objeto_id,
            'form-documento': form_documento.serialize()},
    type: 'POST',
    dataType: 'json',
    beforeSend: function(request) {
        request.setRequestHeader("X-CSRFToken", csrftoken);
        },
    success: function (data) {
        if(data.documento_modal != undefined){
            $('#create-update-ltm-modal').html(data.documento_modal);
            $('#create-update-ltm-modal').modal('show');
            $('.js-btn-documento-edit-ltm-acao').unbind('click');
            $('.js-btn-documento-edit-ltm-acao').click(acaoEditDocumentoLTM); 
        }else if(data.operacao_documento_list != undefined){
            $("#operacao-documento-list").html(data.operacao_documento_list);
        }else if(data.objeto_documento_list != undefined){
            $("#objeto-documento-list").html(data.objeto_documento_list);
        }
        $('#create-update-ltm-modal').modal('hide');
        relink_ltm();
        setCtrl('edit','epim')
        alerta(data);

    }
});
}

var listDocument = function(){
    var url=$(this).data('url');
    var page=$(this).data('page');
    carregarDocumentos(url,page)
}

var carregarDocumentos = function(url,page){
    var form_list_documento = $('#form-add-remove-documento');
    console.log('url '+url+'; page '+page)
    $.ajax({
    url: url,
    type: 'get',
    data: form_list_documento.serialize()+'&page='+page,
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
        $('#resultado-pesquisa-documento').html(data.resultado_pesquisa_documento)
        $('.js-btn-documento-list-filter').unbind('click');
        $('.js-btn-documento-list-filter').click(listDocument)
        $('.js-btn-documento-acao').unbind('click');
        $('.js-btn-documento-acao').click(modalEditDocumento);    
        alerta(data);
        $('.js-btn-documento-edit-ltm-acao').unbind('click');
        $('.js-btn-documento-edit-ltm-acao').click(acaoEditDocumentoLTM); 
    }
    });
}

var modalDocumento = function(){
    $.ajax({
    url: $(this).data('url'),
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
        $('#create-update-ltm-modal').html(data.documento_modal);
        $('.js-btn-documento-list-filter').click(listDocument)
        $('#create-update-ltm-modal').modal('show');
        $('.js-btn-documento-acao').click(modalEditDocumento);
        alert_modal(data);
        $('.js-btn-documento-edit-ltm-acao').unbind('click');
        $('.js-btn-documento-edit-ltm-acao').click(acaoEditDocumentoLTM); 
    }
    });
}

/* Gestao documentos */
var acaoEditDocumento = function(){
    form_documento = $('#form-create-edit-documento')
    operacao = $('#operacao-select').val()
    documento_data = {
    'form-documento': form_documento.serialize(), 
    }
    console.log(form_documento)
    const csrftoken = getCookie('csrftoken');       
    $.ajax({
        url: $(this).data('url'),
        data: documento_data,
        type: 'POST',
        dataType: 'json',
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (data) {
        $("#operacao-documento-list").html(data.operacao_documento_list);
        $('#create-update-modal').modal('hide');
        alerta(data);
    }
    });
    carregarDocumentos("documento-list","1");
};

var modalEditDocumento = function(){
    $.ajax({
    url: $(this).data('url'),
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
        $('#create-update-modal').html(data.documento_modal);
        $('#create-update-modal').modal('show');
        $('.js-btn-documento-edit-acao').unbind('click');
        $('.js-btn-documento-edit-acao').click(acaoEditDocumento);
        alerta(data);
    }
    });
}