var acaoSelectPergunta = function(){
  var url = $(this).data('url')
  console.log('acaoSelectPergunta')
  
  $.ajax({
    url: url,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
        $('#select-modal').modal('hide');
        $('#rotapergunta-id').val(data.pk)
        $('#rotapergunta-denominacao').val(data.pergunta_denominacao)
        $('#grupo-resposta').val(data.grupo_respostas_codigo)
        $('#rotaslimites-id').val(data.rotaslimites_id)
        $('#limiteinferior-id').val(data.limiteinferior)
        $('#limitesuperior-id').val(data.limitesuperior)
        $('#valorteorico-id').val(data.valorteorico)
        $('#unidademedida-limites-id').val(data.unidademedida_fk).change()
        $('#unidademedida-limites-id').selectpicker()
        $('#textolongo-pergunta-id').val(data.textolongo)
        alerta(data);
    }
  });

}


var modalPergunta = function(){
    $.ajax({
      url: $(this).data('url'),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
      },
      success: function (data) {
        $('#create-update-ltm-modal').html(data.pergunta_modal);
        $('#unidademedida-limites-id').selectpicker();
        $('#create-update-ltm-modal').modal('show');
        $('.js-acao-pergunta').click(acaoPergunta);
        $('.js-btn-acao-select-pergunta').click(modalPerguntaSel) //acao selecao nm
        alert_modal(data);
      }
    });
  }

  var listPergunta = function(){
    var url=$(this).data('url');
    var page=$(this).data('page');
    carregarPergunta(url,page)
  }


  var modalEditPergunta = function(){
    console.log($(this).data('url'))
    $.ajax({
      url: $(this).data('url'),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
      },
      success: function (data) {
        $('#modal-3').html(data.pergunta_cadastro_modal);
        $('#modal-3').modal('show');
        $('#cadastro-pergunta-denominacao-id').selectpicker()
        $('#cadastro-pergunta-unidademedida-id').selectpicker()
        $('#cadastro-pergunta-gruporesposta-id').selectpicker()
        $('.js-acao-pergunta-cadastro').click(acaoPerguntaCadastro);
      }
    });
  }

  var carregarPergunta = function(url,page){
    var form_list_pergunta = $('#form-add-remove-pergunta');
    console.log(form_list_pergunta.serialize())
    console.log('url '+url+'; page '+page)
    var sel = $('#sel-id').attr('sel');
    $.ajax({
    url: url,
    type: 'get',
    data: form_list_pergunta.serialize()+'&page='+page+'&sel='+sel,
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
        $('#resultado-pesquisa-pergunta').html(data.resultado_pesquisa_pergunta)
        //filtro perguntas
        $('.js-btn-pergunta-list-filter').unbind('click');
        $('.js-btn-pergunta-list-filter').click(listPergunta)  
        //crud perguntas
        $('.js-btn-pergunta-acao').unbind('click');
        $('.js-btn-pergunta-acao').click(modalEditPergunta)  
        //selecionar pergunta
        $('.js-pergunta-select-ltm-acao').unbind('click');
        $('.js-pergunta-select-ltm-acao').click(acaoSelectPergunta);  
        alerta(data);
    }
    });
  }
  
  var modalPerguntaCadastro = function(){
    $.ajax({
    url: $(this).data('url'),
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
        $('#select-modal').html(data.pergunta_sel_modal);
        $('.js-btn-pergunta-list-filter').click(listPergunta)
        $('.js-btn-pergunta-acao').click(modalEditPergunta)  
        $('#select-modal').modal('show');
        alert_modal(data);
        $('.js-pergunta-select-ltm-acao').unbind('click');
        $('.js-pergunta-select-ltm-acao').click(acaoSelectPergunta);  
        $('#id_gruporespostas_fk').selectpicker("refresh");
    }
    });
  }

  var modalPerguntaSel = function(){
    $.ajax({
    url: $(this).data('url'),
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
        $('#select-modal').html(data.pergunta_sel_modal);
        $('.js-btn-pergunta-list-filter').click(listPergunta)
        $('.js-btn-pergunta-acao').click(modalEditPergunta)  
        $('#select-modal').modal('show');
        alert_modal(data);
        $('.js-pergunta-select-ltm-acao').unbind('click');
        $('.js-pergunta-select-ltm-acao').click(acaoSelectPergunta);  
        $('#id_gruporespostas_fk').selectpicker("refresh");
    }
    });
  }

  var acaoPergunta = function(){
    form_pergunta = $('#form-create-edit-pergunta')
    operacao = $('#operacao-select').val()
    pergunta_data = {
      'form-pergunta': form_pergunta.serialize(), 
    }
    console.log(pergunta_data)
    const csrftoken = getCookie('csrftoken');       
    $.ajax({
        url: $(this).data('url'),
        data: pergunta_data,
        type: 'POST',
        dataType: 'json',
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", csrftoken);
          },
        success: function (data) {
          $("#operacao-pergunta-list").html(data.operacao_pergunta_list);
          relink_ltm();
          $('#create-update-ltm-modal').modal('hide');
          alerta(data);
          setCtrl('edit','epim');
      }
    });
  };

  var acaoPerguntaCadastro = function(){
    form_pergunta = $('#form-pergunta-cadastro')
    pergunta_data = {
      'form-pergunta': form_pergunta.serialize(), 
    }
    console.log(pergunta_data)
    const csrftoken = getCookie('csrftoken');       
    $.ajax({
        url: $(this).data('url'),
        data: pergunta_data,
        type: 'POST',
        dataType: 'json',
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", csrftoken);
          },
        success: function (data) {
          //$("#operacao-pergunta-list").html(data.operacao_pergunta_list);
          //relink_ltm();
          $('#modal-3').modal('hide');
          alerta(data);
          //setCtrl('edit');
          carregarPergunta('pergunta-list',1)
      }
    });
  };


