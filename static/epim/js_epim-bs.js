function refresh(){
  setTimeout(function () {
    location.reload()
  },100);
};

function resizeTextarea(id){
  var element = document.getElementById(id)
  if (typeof(element)!='undefined' && element!=null){
    var s_height = element.scrollHeight;
    element.setAttribute('style','height:'+s_height+'px');
  }
};

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
};

function isEmpty(str){
  return (!str || 0===str.length);
};

function alert_modal(data){
  if (!isEmpty(data.alert_text)){
    $("#modal-alert-title").text(data.alert_title)
    $("#modal-alert-text").text(data.alert_text)
    $("#modal-alert").modal("show");
  };
};

function alerta(data) {
  if (!isEmpty(data.alert_text)){
    let classe = ""
    $('#tile-alert').removeClass();
    $('#alert-strong-text').text(data.alert_title + ": ")
    $('#alert-text').text(data.alert_text)
    switch(data.alert_type){
      case 'erro':
        classe = "alert alert-danger alert-fixed"
        break;
      case 'sucesso':
        classe = "alert alert-success alert-fixed"
        break;
      default:
        classe = "alert alert-warning alert-fixed"
    }
    $('#tile-alert').addClass(classe);
    $('#tile-alert').fadeIn(1000);
    setTimeout(function() { 
        $('#tile-alert').fadeOut(1000); 
    }, 3000);
  };
};


$(document).ajaxStart(
  function(){
    $('.overlay').show()
  }).ajaxSuccess(function(){
    $('.overlay').hide()
  });


