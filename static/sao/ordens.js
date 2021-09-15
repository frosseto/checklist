$(function () {

  /* Functions */

  // var loadForm = function () {
  //   var btn = $(this);
  //   $.ajax({
  //     url: btn.attr("data-url"),
  //     type: 'get',
  //     dataType: 'json',
  //     beforeSend: function () {
  //       $("#modal-uep .modal-content").html("");
  //       $("#modal-uep").modal("show");
  //     },
  //     success: function (data) {
  //       $("#modal-uep .modal-content").html(data.html_form);
  //     }
  //   });
  // };

// function refresh(){
//     setTimeout(function () {
//       location.reload()
//     },100);
// }

  // var saveForm = function () {
  //   var form = $(this);
  //   $.ajax({
  //     url: form.attr("action"),
  //     data: form.serialize(),
  //     type: form.attr("method"),
  //     dataType: 'json',
  //     success: function (data) {
  //       if (data.form_is_valid) {
  //         $("#uep-table tbody").html(data.html_uep_list);
  //         $("#modal-uep").modal("hide");
  //       }
  //       else {
  //         $("#modal-uep .modal-content").html(data.html_form);
  //       }
  //     }
  //   });
  //   refresh();
  //   return false;
  // };


  /* Binding */

  // // Create uep
  // $(".js-create-uep").click(loadForm);
  // $("#modal-uep").on("submit", ".js-uep-create-form", saveForm);

  // // Update uep
  // $("#uep-table").on("click", ".js-update-uep", loadForm);
  // $("#modal-uep").on("submit", ".js-uep-update-form", saveForm);

  // // Delete uep
  // $("#uep-table").on("click", ".js-delete-uep", loadForm);
  // $("#modal-uep").on("submit", ".js-uep-delete-form", saveForm);

});