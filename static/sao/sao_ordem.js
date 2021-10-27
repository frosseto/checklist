function expandTextarea(id) {
  document.getElementById(id).addEventListener('input', function() {
    this.style.overflow = 'hidden';
    this.style.height = 0;
    this.style.height = this.scrollHeight + 'px';
  }, false);
};

function resizeTextarea(id){
  var s_height = document.getElementById(id).scrollHeight;
  document.getElementById(id).setAttribute('style','height:'+s_height+'px');
};

resizeTextarea('id_observacaoanalista');
resizeTextarea('id_observacaoop');
resizeTextarea('id_observacaolocal');

$(document).ready(function(){
    // Add minus icon for collapse element which is open by default
    $(".collapse.show").each(function(){
        $(this).prev(".card-header").find(".fa").addClass("fa-minus").removeClass("fa-plus");
    });
    
    // Toggle plus minus icon on show hide of collapse element
    $(".collapse").on('show.bs.collapse', function(){
        $(this).prev(".card-header").find(".fa").removeClass("fa-plus").addClass("fa-minus");
    }).on('hide.bs.collapse', function(){
        $(this).prev(".card-header").find(".fa").removeClass("fa-minus").addClass("fa-plus");
    });


});



function goBack(){
    window.history.back();
}

$(function () {

  /* Editar */
  var checkSAO = function () {
    var btn = $(this);
    console.log(btn)
    $.ajax({
    url: btn.attr("data-url"),
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
      
    },
    success: function (data) {
        $("#alerta-titulo").text(data.titulo);
        $("#alerta-texto").text(data.msg);
        $("#modal-alert").modal("show");
        if(data.estado_edicao == 'Libe'){
            $("#id_executadopor").prop('readonly',false);
            $("#id_encerradotecnicamentepor").prop('readonly',false);
            $("#id_confirmadopor").prop('readonly',false);
            $('input[name^="lv_"]').prop('disabled',false);
            $('a[name="cancelar"]').show();
            $('button[name="salvar"]').show();
            $('button[name="editar"]').hide();
            $('#btn_estou_com_sorte').hide();
            $("#id_status").val(data.status);
            $('#equipamento').prop('disabled',false);
            $('#equipamento').attr('readonly',false);
            $('#n_testes_val').prop('disabled',false);
            $('#n_falhas_val').prop('disabled',false);
            $('.js-adicionar-obs').show();
        }
      //$("#modal-uep .modal-content").html(data.html_form);
    }
    });
  };

  /* Recarregar */
  function refresh(){
      setTimeout(function () {
        location.reload()
      },100);
  }

  /* Obter valor do cookie name */
  function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }

  /* Salvar */
  var saveSAO = function () {
    var btn = $(this);
    var form = $('#sao-form');
    const csrftoken = getCookie('csrftoken');
    console.log(csrftoken)
    console.log(form)
    $.ajax({
        url: btn.attr("data-url"),
        data: form.serialize(),
        type: 'POST',
        dataType: 'json',
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", csrftoken);
          },
        success: function (data) {
            console.log('resultado: ' + data.resultado)
            $("#id_executadopor").prop('readonly',true);
            $("#id_encerradotecnicamentepor").prop('readonly',true);
            $("#id_confirmadopor").prop('readonly',true);
            $('input[name^="lv_"]').prop('disabled',true);
            $('a[name="cancelar"]').hide();
            $('button[name="salvar"]').hide();
            $('button[name="editar"]').show();
            $('#btn_estou_com_sorte').show();
            $("#alerta-titulo").text(data.titulo);
            $("#alerta-texto").text(data.msg);
            $("#id_status").val(data.status);
            $("#modal-alert").modal("show");
            $("#id_resultado").val(data.resultado);
            $('#equipamento').prop('disabled',true);
            $('#equipamento').attr('readonly',true);
            $('#n_testes_val').prop('disabled',true);
            $('#n_falhas_val').prop('disabled',true);
            $('.js-adicionar-obs').hide();

      }
    });
  };
    
  var adicionarObs = function(){
    var btn = $(this);
    tipo = btn.attr('tipo');
    console.log(tipo)
    switch(tipo){
      case 'observacaolocal':
        $('#obs-modal-title').text('Observação EPIM (interna)');
        break;
      case 'observacaoanalista':
        $('#obs-modal-title').text('Observação Analista');
        break;
    };
    $('#obs-modal-text').val('')
    $('.js-adicionar-inc').attr('tipo',tipo)
    $('#obs-modal').modal('show');
  };

  var incluirObs = function(){
    var btn = $(this);
    tipo = btn.attr('tipo');
    console.log(tipo)
    var user = $('#user').text();
    var data = moment(Date()).format('DD/MM/YYYY h:mm:ss');
    var txt
    if($('#id_' + tipo).val()){
      txt = '\n'
    }
    else{
      txt = ''
    }
    $('#id_' + tipo).val($('#id_' + tipo).val() + txt + data + ' ' + user + ': ' + $('#obs-modal-text').val())
    $('#obs-modal').modal('hide');
    resizeTextarea('id_observacaoanalista');
    resizeTextarea('id_observacaoop');
    resizeTextarea('id_observacaolocal');

  };
  
  
  /* Binding */
  $(".js-edit-sao").click(checkSAO);
  $(".js-save-sao").click(saveSAO);
  $("#sao-form").on("submit", ".js-save-sao", saveSAO);
  $(".js-adicionar-obs").click(adicionarObs);
  $(".js-adicionar-inc").click(incluirObs);
  });