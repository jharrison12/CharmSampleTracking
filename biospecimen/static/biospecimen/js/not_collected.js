//Hide other specify input box
$('#other_specify_input').parent().hide();


$('#id_not_collected_form-refused_other_1').click(function() {
  $('#other_specify_input').parent()[this.checked ? "show" : "hide"]();
});


$('#id_not_collected_form-refused_other_0').click(function() {
  $('#other_specify_input').parent().hide();
});