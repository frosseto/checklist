/* Seta visibilidade dos btns de acao */
var setCtrl = function(status,perfil=null){
  var classe = $('#classe-denominacao').attr('classe_pk')
  var objeto = $('#objeto-denominacao').attr('objeto_pk')
  var operacao = $('#operacao-select').val() /*operação id*/

  console.log("Classe: ",classe,"; Objeto: ",objeto,"; Operação:",operacao,"; Status: ",status,"; Perfil: ",perfil)

  $('.js-btn-edit-ltm').hide(); /* btn acao ltm - operacao e objeto*/
  $('.operacao-edit').hide();  /* btn acao operacao - material, documento, norma */
  $('.objeto-edit').hide(); /* btn acao objeto - documento */
  $('.js-adicionar-obs').hide();
 
  switch(status) {
    case 'edit':
      if(!!classe && !!operacao && perfil=='epim'){  
          $('.operacao-edit').show();   
      } 
      if(!!objeto && perfil=='epim'){
          $('.objeto-edit').show();
      }
      if(!!objeto || !!operacao){
        if (perfil=='epim' || perfil=='operacao'){
          $('.js-btn-edit-ltm[name="cancelar"]').show();
          $('.js-btn-edit-ltm[name="salvar"]').show(); 
          $('.js-adicionar-obs').show();
        }
        if (perfil=='epim'){
          $('#rotas-pergunta-sort').removeClass('default')
          $('#rotas-pergunta-sort').addClass('grab')
          if ( $("#rotas-pergunta-sort tbody").sortable()){ 
            $("#rotas-pergunta-sort tbody").sortable("enable");
          }
        }
      }
      if (perfil=='epim'){
        readonly=false;
      } else {
        readonly=true;
      }
      break;
    default:
      if(!!classe){
        $('.js-btn-edit-ltm[name="adicionar-classe-herdada"]').show();
        $('.js-btn-edit-ltm[name="operacao-adicionar"]').show();
        
        $('#dropdownClasse').show();
        $('#btn-classe-create2').hide();

        if(!!operacao){
          $('#dropdownOperacao').show();
          $('#rotas-pergunta-sort').removeClass('grab')
          $('#rotas-pergunta-sort').addClass('default')
          if ( $("#rotas-pergunta-sort tbody").sortable()){ 
            $("#rotas-pergunta-sort tbody").sortable("disable");
          }
          $('.js-btn-edit-ltm[name="operacao-adicionar"]').show();
          $('.js-btn-edit-ltm[name="operacao-adicionar2"]').hide();
          $('.js-btn-edit-ltm[name="operacao-editar-tipo"]').show();
          $('.js-btn-edit-ltm[name="operacao-inativar"]').show();
        } else{
          $('.js-btn-edit-ltm[name="adicionar-op"]').show();
          $('.js-btn-edit-ltm[name="operacao-adicionar2"]').show();
          $('#dropdownOperacao').hide();
        }
      }else{
        $('#dropdownOperacao').hide();
        $('#dropdownClasse').hide();
        $('#btn-classe-create2').show();
      }
      if(!!objeto || !!operacao){
        $('.js-btn-edit-ltm[name="editar"]').show();
      }
      if(!!objeto){
        $('.js-btn-edit-ltm[name="objeto-alterar-classe"]').show();
        $('.js-btn-edit-ltm[name="objeto-alterar-referencia"]').show();
      }
      readonly=true
    };
  $('.edit-ltm').prop('disabled',readonly);
  $('.edit-ltm').attr('readonly',readonly); 

  /* bloquear alteracao de operacao enquanto edicao, 
  em edicao, permitir alterar o status da operacao e do objeto */
  if(status=='edit'){
    $("#operacao-select").prop("disabled", true);
    $("#operacao-select").addClass("disabled");
    $("#operacao-status-select").prop("disabled", false);
    $("#operacao-status-select").removeClass("disabled");
    $("#objeto-status-select").prop("disabled", false);
    $("#objeto-status-select").removeClass("disabled");
  } else{
    $("#operacao-select").prop("disabled", false);
    $("#operacao-select").removeClass("disabled");
    $("#operacao-status-select").prop("disabled", true);
    $("#operacao-status-select").addClass("disabled");
    $("#objeto-status-select").prop("disabled", true);
    $("#objeto-status-select").addClass("disabled");
  }

  $('.selectpicker').selectpicker('refresh');
  relink_ltm();
};

/* Relink dos resultados da selecao */
function relink(){
  $(".js-ltm-list").unbind("click");
  $(".js-ltm-list").click(loadObjetoClasse);
  $('.js-btn-objeto-selecao-list-filter').click(loadObjetoClasseList); //btn pesquisar classe/objeto
};

function relink_ltm(){
  $(".js-adicionar-obs").unbind('click');
  $(".js-adicionar-obs").click(adicionarObs);

  $('.js-btn-acao-material').unbind('click');
  $('.js-btn-acao-material').click(modalMaterial);
  $('.js-btn-acao-select-nm').unbind('click'); /* incluir nm */
  $('.js-btn-acao-select-nm').click(modalMaterialNM);

  $('#operacao-select').unbind('change');
  $('#operacao-select').on('change',loadOperacaoData); 
  $('#operacao-select').selectpicker("refresh");
  $('#operacao-status-select').selectpicker("refresh");
  $('#operacao-executante').selectpicker("refresh");
  $("#objeto-status-select").selectpicker("refresh");
  
  $('.js-btn-documento-ltm-acao').unbind('click'); /* incluir documento */
  $('.js-btn-documento-ltm-acao').click(modalDocumento);
  $('.js-btn-documento-edit-ltm-acao').unbind('click'); /* acoes edit/delete */
  $('.js-btn-documento-edit-ltm-acao').click(acaoEditDocumentoLTM); 

  $('.js-btn-pergunta-ltm-acao').unbind('click'); /* associar pergunta com a operacao */
  $('.js-btn-pergunta-ltm-acao').click(modalPergunta);
  $('.js-btn-acao-select-pergunta').unbind('click'); /* selecionar pergunta */
  $('.js-btn-acao-select-pergunta').click(modalPerguntaSel);

  $('.js-btn-norma-ltm-acao').unbind('click');
  $('.js-btn-norma-ltm-acao').click(modalNorma);
  $('.js-btn-norma-edit-ltm-acao').unbind('click');
  $('.js-btn-norma-edit-ltm-acao').click(acaoEditNormaLTM); 

  $('.js-btn-classe-edit-ltm-acao').unbind('click');
  $('.js-btn-classe-edit-ltm-acao').click(acaoSelectClasse); 
  
  $("select[name^='if_']").selectpicker("refresh");
  $("select[name^='unidade']").selectpicker("refresh");
}
 
/* Ações disparadas por botões da classe js-btn-edit-ltm */
var acaoLTM = function(){

  var item = $(this);
  var url = $(this).data('url')
  var acao = item.attr('name') 
  var classe = $('#classe-denominacao').attr('classe_pk')
  var operacao = $('#operacao-select').val()

  switch (acao){
    case 'editar':
      editLTM();
      break;
    case 'cancelar':
      cancelEditLTM();
      break;
    case 'salvar':
      saveLTM();
      break;
    case 'operacao-inativar':
      $("#modal-confirm").modal('show');
      $("#modal-confirm-btn").unbind("click");
      $("#modal-confirm-btn").bind("click",function(){
        $("#titulo-confirmacao").text('Confirmar exclusão');
        $("#body-confirmacao").text(' Tem certeza que deseja excluir?');
        inativarOp()
      });
      break;
    case 'operacao-adicionar':
      modalOperacao(url,acao,classe,operacao);
      break;
    case 'operacao-adicionar2':
      modalOperacao(url,acao,classe,operacao);
      break;
    case 'operacao-editar-tipo':
      modalOperacao(url,acao,classe,operacao);
      break;
    case 'adicionar-classe-herdada':
      selectClasse(url);
      break;
    case 'objeto-alterar-classe':
      var objeto_id = $('#objeto-denominacao').attr('objeto_pk')
      selectClasse(url+'?objeto='+objeto_id);
      break;
    case 'objeto-alterar-referencia':
      var objeto_id = $('#objeto-denominacao').attr('objeto_pk')
      selectObjetoReferencia(url+'?objeto='+objeto_id);
      break;   
    default:
      console.log(acao + ' - ação não implementada');
  }
};


/* ====================== Acoes LTM ========================*/
var editLTM = function(){
  var classe = $('#classe-denominacao').attr('classe_pk')
  var operacao = $('#operacao-select').val()
  var objeto = $('#objeto-denominacao').attr('objeto_pk')

  var ltm_data = {
    'classe': classe,
    'operacao': operacao,
    'objeto': objeto,
    'edit': 'editar'
  }
  
  const csrftoken = getCookie('csrftoken'); 
  console.log('edit');      
  $.ajax({
      url: "/saem/ltm/edit",
      data: ltm_data,
      type: 'POST',
      dataType: 'json',
      beforeSend: function(request) {
          request.setRequestHeader("X-CSRFToken", csrftoken);
      },
      success: function (data) {
        console.log(data.msg)  
        alerta(data);
        setCtrl('edit',data.perfil);
      }
  });

};

var cancelEditLTM = function(){
  var classe = $('#classe-denominacao').attr('classe_pk')
  var operacao = $('#operacao-select').val()
  var objeto = $('#objeto-denominacao').attr('objeto_pk')
  var ltm_data = {
    'classe': classe,
    'operacao': operacao,
    'objeto': objeto,
    'edit': 'cancel',
  }
  const csrftoken = getCookie('csrftoken'); 
  console.log('cancel');      
  $.ajax({
      url: "/saem/ltm/edit",
      data: ltm_data,
      type: 'POST',
      dataType: 'json',
      beforeSend: function(request) {
          request.setRequestHeader("X-CSRFToken", csrftoken);
      },
      success: function (data) {
        alerta(data);
        setCtrl();
      }
  });
};

var saveLTM = function(){
  var classe = $('#classe-denominacao').attr('classe_pk')
  var operacao = $('#operacao-select').val()
  var form_operacao = $('#form-operacao');
  var objeto = $('#objeto-denominacao').attr('objeto_pk')
  var form_local = $('#form-local');
  var rotas_ordenacao={}
  $("#rotas-pergunta-sort > tbody > tr").each(function(index,tr){
    rotas_ordenacao[index+1]=$(tr).find('td.id').html()
  });

  var ltm_data = {
    'classe': classe,
    'operacao': operacao,
    'operacao-status': $("#operacao-status-select").val(),
    'form-operacao': form_operacao.serialize(),
    'objeto': objeto,
    'objeto-status': $("#objeto-status-select").val(),
    'form-local': form_local.serialize(),
    'rotas_ordenacao': JSON.stringify(rotas_ordenacao),
    'edit': 'save',
  }


  const csrftoken = getCookie('csrftoken'); 
  console.log('save');      
  $.ajax({
      url: "/saem/ltm/save",
      data: ltm_data,
      type: 'POST',
      dataType: 'json',
      beforeSend: function(request) {
          request.setRequestHeader("X-CSRFToken", csrftoken);
      },
      success: function (data) {
        alerta(data);
        $("#classe-denominacao-header").text(data.classe_denominacao)
        $("#classe-status").text(data.classe_status)
        $("#classe-status").css("background-color", "background-color: #"+ data.classe_status_color +" !important;");
        setCtrl();
      }
  });
};

var inativarOp = function(){
  var classe = $('#classe-denominacao').attr('classe_pk')
  var operacao = $('#operacao-select').val()
  var ltm_data = {
    'classe': classe,
    'operacao': operacao,
    'edit': 'operacao-inativar',
  }
  const csrftoken = getCookie('csrftoken');      
  $.ajax({
      url: "/saem/ltm/edit",
      data: ltm_data,
      type: 'POST',
      dataType: 'json',
      beforeSend: function(request) {
          request.setRequestHeader("X-CSRFToken", csrftoken);
      },
      success: function (data) {
        loadData(tipo='classe',valor=classe,url="/saem/ltm")
        alert_modal(data);
        setCtrl();
        $("#modal-confirm").modal('hide');
      }
  });
};


//ordenacao rotas
var fixHelperModified = function(e, tr) {
  var $originals = tr.children();
  var $helper = tr.clone();
  $helper.children().each(function(index) {
      $(this).width($originals.eq(index).width())
  });
  return $helper;
  },
  updateIndex = function(e, ui) {
      $('td.index', ui.item.parent()).each(function (i) {
          $(this).html(i + 1);
      });
  };


/* seta elementos da aplicacao com os dados operacao/objeto */
var loadDataOperacao = function(data){
  /* dados de operacoes */
  $("#operacao-duracao").val(data.operacao_duracao);
  $("#operacao-qde-executantes").val(data.operacao_qde_executantes);
  $("#operacao-executante").val(data.executante_fk)
  $("#operacao-executante").selectpicker('refresh')
  /* aba operacoes */
  $("#operacao-texto").html(data.operacao_texto);
  $("#operacao-pergunta-list").html(data.operacao_pergunta_list);

  $("#rotas-pergunta-sort tbody").sortable({
    helper: fixHelperModified,
    stop: updateIndex
  }).disableSelection();

  if ( $("#rotas-pergunta-sort tbody").sortable()){ 
    $("#rotas-pergunta-sort tbody").sortable("disable");
  }

  $("#operacao-material-list").html(data.operacao_material_list);
  $("#operacao-documento-list").html(data.operacao_documento_list);
  $("#operacao-norma-list").html(data.operacao_norma_list);
  $("#operacao-observacao").html(data.operacao_observacao);
  $("#operacao-status-select").html(data.operacao_status_select);
  $("#operacao-status-select").selectpicker('refresh')
  $("#operacao-if-frequencia-list").html(data.operacao_if_frequencia);
  $("#classe-denominacao-header").text(data.classe_denominacao)
  $("#classe-status").text(data.classe_status)
  $("#classe-status").css("background-color", "background-color: #"+ data.classe_status_color +" !important;");
  /* aba objeto */
  $('#objeto-tipo-acesso-cb').html(data.objeto_tipo_acesso);
  $('#obj-localizacao-campos').html(data.objeto_localizacao);
  $("#objeto-documento-list").html(data.objeto_documento_list);
  $("#obj-calibracao-campos").html(data.objeto_calibracao);
  $("#objeto-observacao-texto").html(data.objeto_obs);
  /* ajuste altura text areas */
  resizeTextarea("operacao-texto-textarea");
  resizeTextarea("operacao-observacao-textarea");  
  resizeTextarea("objeto-observacao-textarea"); 
  relink_ltm();
}


/* carrega dados */
var loadData = function(tipo,valor,url){
  $.ajax({
    url: url,
    data: { tipo: tipo, valor: valor},
    type: 'GET',
    dataType: 'json',
    success: function (data) { 
      $('#classe-denominacao').text(data.classe)
      $('#classe-denominacao').attr('classe_pk',data.classe_id)
     /* $('#classe-denominacao').attr('title',data.classe_heranca) */
      $('#btn-classe-update').data('id',data.classe_id);
      $('#btn-classe-delete').data('id',data.classe_id);
      $('#classe-principal-selecionada').text(data.classe)
      $('#classes-herdadas-list').html(data.classe_herdada_list)
      $("#operacao-select").html(data.operacao_select);
      $("#operacao-status-select-div").html(data.operacao_status_select);
      $('#atribuicao-automatica-div').html(data.atribuicao_automatica);

      if(data.atribuicao_automatica!=undefined){
        $('.js-btn-atribuicao-automatica-list-filter').unbind('click');
        $('.js-btn-atribuicao-automatica-list-filter').click(listAtualizacaoautomatica)
        $('.js-btn-atribuicao-automatica-acao').unbind('click');
        $('.js-btn-atribuicao-automatica-acao').click(modalEditAtualizacaoautomatica);  
      };

      if(data.objeto!=undefined){
        $('#objeto-denominacao').html(data.objeto)
        $('#objeto-referencia').html(data.objeto_referencia)
        $('#objeto-denominacao').attr('objeto_pk',data.objeto_id)
        $('#objeto-status-select-div').html(data.objeto_status_select);
        $('#objeto-status-select').selectpicker('refresh')
        $("#objeto-protecaoex").val(data.protecaoex_denominacao);

      }
      
      $("#classe-local").val(data.classe_denominacao);
      
      loadDataOperacao(data);
      relink_ltm();
      alert_modal(data);
      setCtrl('');
    }
  }); 
};

/* Carrega dados de classe/operacao e objeto (conforme tipo de item selecionado) */
var loadObjetoClasse = function () {

  var item = $(this);
  const csrftoken = getCookie('csrftoken');
  var tipo = item.attr('tipo');
  var valor = item.attr('valor');

  if(tipo=='local'){
    $('#tab-local tr').removeClass("bg-primary");
    $('#tab-local tr').removeClass("text-light");
    item.toggleClass('bg-primary');
    item.addClass('text-light');
    $("#form-local").show();
    $("#local-instalacao").val("");
    $("#objeto-tab-nav-item").show();
   // $("#objeto-tab").tab('show');
  }else{
    $('#tab-classe tr').removeClass("bg-primary");
    $('#tab-classe tr').removeClass("text-light");
    item.toggleClass('bg-primary');
    item.addClass('text-light');
    $("#form-local").hide();
    $("#objeto-tab-nav-item").hide();
    $("#classe-operacao-tab").tab('show');
  }
  
  $("#form-operacao").show();

  url = item.attr("data-url");
  loadData(tipo,valor,url);

};

/* ================================================================= */

/* Carrega resultados da pesquisa - objeto e classe */
var loadObjetoClasseList = function () {
  var btn = $(this);
  var page=btn.data('page');

  var form = $('#local-classe-form');
  console.log(form.serialize());
  const csrftoken = getCookie('csrftoken');       
  $.ajax({
    url: "/saem/list",
    data: form.serialize()+'&page='+page,
    type: 'GET', //POST
    dataType: 'json',
    success: function (data) {
      $("#local-lista").html(data.local_html);
      $("#classe-lista").html(data.classe_html);
      $('#tab-local').DataTable({
                  "language": {
                  "search": "Filtrar",
                  "emptyTable": "Nenhum objeto encontrado"
                  },
                  "paging": false,
                  "info":   false,
      });
      relink();
      alerta(data);
    }
  });
};

/* Select operacao */
var loadOperacaoData = function () {
  /* nao executar acao em modo de edicao - salvaguarda de edicao de operacao em andamento */
  if($("button[name='salvar'").is(":visible")){
    $("#save-ok-modal").modal('show');
    return;
  }
  var operacao = $(this).val();
  data_url = '/saem/operacao/'+ operacao + '/'
  console.log('load operacao')
  $.ajax({
    url: data_url,
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
      loadDataOperacao(data);
      alert_modal(data);
    }
  });
  $('#operacao-select').selectpicker("refresh");
  $('#operacao-status-select').selectpicker("refresh");
  $('#operacao-executante').selectpicker("refresh");
};

/* =========================js-adicionar-obs======================================== */
var adicionarObs = function(){
  var btn = $(this);
  tipo = btn.attr('tipo');
  console.log(tipo)
  switch(tipo){
    case 'observacao-operacao':
      $('#obs-modal-title').text('Observação Operação');
      break;
    case 'observacao-objeto':
      $('#obs-modal-title').text('Observação Local');
      break;
  };
  $('#obs-modal-text').val('')
  $('.js-adicionar-inc').attr('tipo',tipo)
  $('#obs-modal').modal('show');
};

var appendObs = function(){
  var btn = $(this);
  tipo = btn.attr('tipo');
  console.log(tipo)
  var user = $('#user').text();
  var data = moment(Date()).format('DD/MM/YYYY h:mm:ss');
  console.log(tipo, $('.' + tipo).val())
  if($('.' + tipo).val()){
    txt = '\n'
  }
  else{
    txt = ''
  }
  $('.' + tipo).val($('.' + tipo).val() + txt + data + ' ' + user + ': ' + $('#obs-modal-text').val())
  $('#obs-modal').modal('hide');

};



/*==============================Operacao============================================*/

/* Cadastro/edicao de operacao */
var acaoOperacao = function(){
  var form_operacao = $('#form-create-edit-operacao')
  var operacao = $('#operacao-select').val()
  var classe = $('#classe-denominacao').attr('classe_pk')
  var item = $(this);
  var acao = item.attr('name') 

  operacao_data = {
    'form-operacao': form_operacao.serialize(), 
    'classe': classe,
    'operacao': operacao,
    'acao': acao,
  }
  console.log(operacao_data)

  const csrftoken = getCookie('csrftoken');       
  $.ajax({
      url: item.data('id'),
      data: operacao_data,
      type: 'POST',
      dataType: 'json',
      beforeSend: function(request) {
          request.setRequestHeader("X-CSRFToken", csrftoken);
        },
      success: function (data) {
        $('#create-update-ltm-modal').modal('hide');
        loadData(tipo='classe',valor=classe,url="/saem/ltm")
        alerta(data)
    }
  });
};

/* Modal para cadastro/edicao de operacao */
var modalOperacao = function(url,acao,classe=null,operacao=null){
  $.ajax({
    url: url,
    type: 'get',
    data: {'operacao':operacao, 'classe':classe, 'acao':acao},
    dataType: 'json',
    beforeSend: function () {
    },
    success: function (data) {
      $('#create-update-ltm-modal').html(data.operacao_modal);
      $('#create-update-ltm-modal').modal('show');
      $('.js-acao-operacao').click(acaoOperacao);
      alert_modal(data);
      $("#create-update-ltm-modal").on("shown.bs.modal", function () { 
        $('#tipo-atividade-modal-id').selectpicker("refresh");
      });
    }
  });
}

