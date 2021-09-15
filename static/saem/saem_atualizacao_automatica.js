var listAtualizacaoautomatica = function(){
    var url=$(this).data('url');
    var page=$(this).data('page');
    carregarAtualizacaoautomatica(url,page)
}

var carregarAtualizacaoautomatica = function(url,page){
    var form_list_atribuicao_automatica = $('#form-atribuicao-automatica');
    console.log('url '+url+'; page '+page)
    $.ajax({
    url: url,
    type: 'get',
    data: form_list_atribuicao_automatica.serialize()+'&page='+page,
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
        $('#resultado-pesquisa-atualizacao-automatica').html(data.resultado_atribuicao_automatica_pesquisa)
        $('.js-btn-atribuicao-automatica-list-filter').unbind('click');
        $('.js-btn-atribuicao-automatica-list-filter').click(listAtualizacaoautomatica);
        $('.js-btn-atribuicao-automatica-acao').unbind('click');
        $('.js-btn-atribuicao-automatica-acao').click(modalEditAtualizacaoautomatica);  
        $("form").bind("keypress", function(e){
            if(e.keyCode == 13){
              return false;
            }
          });  
    }
    });
}


/* Gestao documentos */
var acaoEditAtualizacaoautomatica = function(){
  var form_atualizacao_automatica = $('#form-create-edit-atualizacao-automatica');
  var classe = $('#classe-denominacao').attr('classe_pk');
  form_data = {
  'form-atualizacao-automatica': form_atualizacao_automatica.serialize(), 
  }
  console.log(form_atualizacao_automatica);
  const csrftoken = getCookie('csrftoken');     
  $.ajax({
      url: $(this).data('url'),
      data: form_data,
      type: 'POST',
      dataType: 'json',
      beforeSend: function(request) {
          request.setRequestHeader("X-CSRFToken", csrftoken);
      },
      success: function (data) {
      $('#create-update-modal').modal('hide');
      alerta(data);
      },
      complete: function(data){
        carregarAtualizacaoautomatica("atribuicao-automatica-list/"+classe+"/","1");
        $('#create-update-modal').modal('hide');
        alerta(data);
      }
  }); 
};


var modalEditAtualizacaoautomatica = function(){
  $.ajax({
  url: $(this).data('url'),
  type: 'get',
  dataType: 'json',
  beforeSend: function () {
  },
  success: function (data) {
      $('#create-update-modal').html(data.atribuicao_automatica_modal);
      $('#create-update-modal').modal('show');
      $('.js-btn-atribuicao-automatica-edit-acao').unbind('click');
      $('.js-btn-atribuicao-automatica-edit-acao').click(acaoEditAtualizacaoautomatica);
      alerta(data);
  }
  });
}


