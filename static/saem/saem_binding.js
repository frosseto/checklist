$('#btn-objeto-classe-list').click(loadObjetoClasseList); //btn pesquisar classe/objeto
$('#btn-classe-create').click(editClasse); //btn criar classe
$('#btn-classe-update').click(editClasse); 
$('#btn-classe-delete').click(editClasse); 
$('#btn-classe-create2').click(editClasse);


/* btn edicao ltm */
$('.js-btn-edit-ltm').click(acaoLTM);
$('.js-adicionar-obs').click(adicionarObs);
$('.js-adicionar-inc').click(appendObs);
$('.js-btn-acao-select-pergunta').click(modalPerguntaSel);

/* Selecao classes e locais */
$('.campos-objeto-classe-list').on('keypress', function (e) {
  if(e.which === 13){
    var btn = $(this).attr('name')
    console.log(btn)
    /* ao pesquisar por local ou denominacao, selecionar o checkbox pesquisar obj e selecionar aba conforme o caso */
    if (['denominacao','locinstalacao','tag'].includes(btn)){
      $('input[name="cb-pesquisar-obj"]').prop('checked',true)
      $('#local-tab').tab('show')
    } else if (btn == 'classemanut') {
      /*$('#classe-tab').tab('show')*/
    }
    loadObjetoClasseList()
  }
});

$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
  console.log(e.target.id);
  if (['texto-operacao-tab-link','observacao-operacao-link','observacao-objeto-link'].includes(e.target.id)){
    resizeTextarea("operacao-texto-textarea");
    resizeTextarea("operacao-observacao-textarea");
    resizeTextarea("objeto-observacao-textarea");
  }
});

$(document).ready(function(){
  $("#form-atribuicao-automatica").bind("keypress", function(e){
    if(e.keyCode == 13){
      return false;
    }
  });
});