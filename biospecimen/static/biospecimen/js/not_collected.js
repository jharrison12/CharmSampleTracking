//Hide other specify input box
$('#other_specify_input').parent().hide();

console.log('reached this');

$('#id_not_collected_form-refused_or_other_1').click(function() {
  $('#other_specify_input').parent().show();
});

$('#id_not_collected_form-refused_or_other_0').click(function() {
  $('#other_specify_input').parent().hide();
});