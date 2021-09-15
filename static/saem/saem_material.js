var acaoMaterial = function(){
  form_material = $('#form-create-edit-material')
  operacao = $('#operacao-select').val()
  material_data = {
    'form-material': form_material.serialize(), 
  }
  console.log(form_material)
  const csrftoken = getCookie('csrftoken');       
  $.ajax({
      url: $(this).data('url'),
      data: material_data,
      type: 'POST',
      dataType: 'json',
      beforeSend: function(request) {
          request.setRequestHeader("X-CSRFToken", csrftoken);
        },
      success: function (data) {
        $("#operacao-material-list").html(data.operacao_material_list);
        relink_ltm();
        $('#create-update-ltm-modal').modal('hide');
        alerta(data);
        setCtrl('edit','epim');
    }
  });
};
  

var modalMaterial = function(){
  $.ajax({
    url: $(this).data('url'),
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
      $('#create-update-ltm-modal').html(data.material_modal);
      $('#create-update-ltm-modal').modal('show');
      $('.js-acao-material').click(acaoMaterial); //acao edicao material
      $('.js-btn-acao-select-nm').click(modalMaterialNM) //acao selecao nm
      alert_modal(data);
    }
  });
}



/* Selecao NM */
var acaoSelectMaterialNM = function(){
  var url = $(this).data('url')
  console.log(url)
  
  $.ajax({
    url: url,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
        $('#select-modal').modal('hide');
        $('#nm-form-modal').val(data.nm)
        $('#denominacao-modal-id').val(data.textobrevematerial)
        $('#unidade-modal-id').val(data.unidade)
        alerta(data);
    }
  });

}


var carregarNMs = function(url,page){
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
      $('.js-btn-material-list-filter').unbind('click');
      $('.js-btn-material-list-filter').click(listMaterialNM)  
      $('.js-material-nm-ltm-acao').unbind('click');
      $('.js-material-nm-ltm-acao').click(acaoSelectMaterialNM);  
      alerta(data);
  }
  });
}

var listMaterialNM = function(){
  var url=$(this).data('url');
  var page=$(this).data('page');
  carregarNMs(url,page)
}

var modalMaterialNM = function(){
  $.ajax({
  url: $(this).data('url'),
  type: 'get',
  dataType: 'json',
  beforeSend: function () {
  },
  success: function (data) {
      $('#select-modal').html(data.documento_modal);
      $('.js-btn-material-list-filter').click(listMaterialNM)
      $('#select-modal').modal('show');
      alert_modal(data);
      $('.js-material-nm-ltm-acao').unbind('click');
      $('.js-material-nm-ltm-acao').click(acaoSelectMaterialNM);
  }
  });
}