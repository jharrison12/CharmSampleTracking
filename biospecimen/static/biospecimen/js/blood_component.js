//Hid component if not clicked
$('#whole_blood_number_of_tubes_div').hide();
$('#serum_number_of_tubes_div').hide();
$('#plasma_number_of_tubes_div').hide();
$('#red_blood_cells_number_of_tubes_div').hide();
$('#buffy_coat_number_of_tubes_div').hide();

console.log('reached this')
$('#id_blood_form-whole_blood').click(function() {
  $('#whole_blood_number_of_tubes_div')[this.checked ? "show" : "hide"]();
});
$('#id_blood_form-serum').click(function() {
  $('#serum_number_of_tubes_div')[this.checked ? "show" : "hide"]();
});
$('#id_blood_form-plasma').click(function() {
  $('#plasma_number_of_tubes_div')[this.checked ? "show" : "hide"]();
});
$('#id_blood_form-buffy_coat').click(function() {
  $('#buffy_coat_number_of_tubes_div')[this.checked ? "show" : "hide"]();
});
$('#id_blood_form-red_blood_cells').click(function() {
  $('#red_blood_cells_number_of_tubes_div')[this.checked ? "show" : "hide"]();
});


// Reload javascript if user hits back button.
$(document).ready(function(e) {
    var $input = $('#refresh');
    $input.val() == 'yes' ? location.reload(true) : $input.val('yes');
});