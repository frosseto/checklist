/* Normas associados com operação */
var acaoEditNormaLTM = function(){
    var operacao_id = $('#operacao-select').val();
    var norma_id = $(this).data('id')
    form_norma = $('#form-update-remove-norma')
    console.log('acaoEditNormaLTM')
    const csrftoken = getCookie('csrftoken'); 
    $.ajax({
    url: $(this).data('url'),
    data:  {'operacao_id': operacao_id, 
            'norma_id': norma_id,
            'form-norma': form_norma.serialize()},
    type: 'POST',
    dataType: 'json',
    beforeSend: function(request) {
        request.setRequestHeader("X-CSRFToken", csrftoken);
        },
    success: function (data) {
        if(data.norma_modal != undefined){
            $('#create-update-ltm-modal').html(data.norma_modal);
            $('#create-update-ltm-modal').modal('show');
            $('.js-btn-norma-edit-ltm-acao').unbind('click');
            $('.js-btn-norma-edit-ltm-acao').click(acaoEditNormaLTM); 
        }else if(data.operacao_norma_list != undefined){
            $("#operacao-norma-list").html(data.operacao_norma_list);
        }
        $('#create-update-ltm-modal').modal('hide');
        relink_ltm();
        setCtrl('edit','epim')
        alerta(data);

        }
    });
}

/* carrega lista de normas pesquisa+paginacao */
var listNorma = function(){
    var url=$(this).data('url');
    var page=$(this).data('page');
    carregarNormas(url,page)
}

var carregarNormas = function(url,page){
    var form_list_norma = $('#form-add-remove-norma');
    console.log('url '+url+'; page '+page)
    $.ajax({
    url: url,
    type: 'get',
    data: form_list_norma.serialize()+'&page='+page,
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
        $('#resultado-pesquisa-norma').html(data.resultado_pesquisa_norma)
        $('.js-btn-norma-list-filter').unbind('click');
        $('.js-btn-norma-list-filter').click(listNorma)
        $('.js-btn-norma-acao').unbind('click');
        $('.js-btn-norma-acao').click(modalEditNorma);    
        alerta(data);
        $('.js-btn-norma-edit-ltm-acao').unbind('click');
        $('.js-btn-norma-edit-ltm-acao').click(acaoEditNormaLTM); 
    }
    });
}

var modalNorma = function(){
    $.ajax({
    url: $(this).data('id'),
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
        $('#create-update-ltm-modal').html(data.norma_modal);
        $('.js-btn-norma-list-filter').click(listNorma)
        $('#create-update-ltm-modal').modal('show');
        $('.js-btn-norma-acao').click(modalEditNorma);
        alert_modal(data);
        $('.js-btn-norma-edit-ltm-acao').unbind('click');
        $('.js-btn-norma-edit-ltm-acao').click(acaoEditNormaLTM); 
    }
    });
}

/* Gestao normas */
var acaoEditNorma = function(){
    form_norma = $('#form-create-edit-norma')
    operacao = $('#operacao-select').val()
    norma_data = {
    'form-norma': form_norma.serialize(), 
    }
    console.log(form_norma)
    const csrftoken = getCookie('csrftoken');       
    $.ajax({
        url: $(this).data('url'),
        data: norma_data,
        type: 'POST',
        dataType: 'json',
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (data) {
        $("#operacao-norma-list").html(data.operacao_norma_list);
        $('#create-update-modal').modal('hide');
        alerta(data);
    }
    });
    carregarNormas("norma-list","1");
};

var modalEditNorma = function(){
    $.ajax({
    url: $(this).data('url'),
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
        $('#create-update-modal').html(data.norma_modal);
        $('#create-update-modal').modal('show');
        $('.js-btn-norma-edit-acao').unbind('click');
        $('.js-btn-norma-edit-acao').click(acaoEditNorma);
        alerta(data);
    }
    });
}