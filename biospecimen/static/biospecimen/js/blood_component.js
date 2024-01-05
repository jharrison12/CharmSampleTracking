//Hid component if not clicked
$('#whole_blood_number_of_tubes_div').hide();
console.log('reached this')
$('#id_blood_form-whole_blood').click(function() {
  $('#whole_blood_number_of_tubes_div')[this.checked ? "show" : "hide"]();
});

// Reload javascript if user hits back button.
$(document).ready(function(e) {
    var $input = $('#refresh');

    $input.val() == 'yes' ? location.reload(true) : $input.val('yes');
});