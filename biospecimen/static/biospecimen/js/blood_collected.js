//Hide component if not clicked
//TODO FIX ALL OF THIS
$('#tube_one_estimated_volume').hide();
$('#tube_two_estimated_volume').hide();
$('#tube_three_estimated_volume').hide();

console.log('reached this')

document.getElementById('id_blood_form-tube_one').addEventListener('change', function () {
    var style = this.value == 'P' ? 'block' : 'none';
    document.getElementById('tube_one_estimated_volume').style.display = style;
});

document.getElementById('id_blood_form-tube_two').addEventListener('change', function () {
    var style = this.value == 'P' ? 'block' : 'none';
    document.getElementById('tube_two_estimated_volume').style.display = style;
});

document.getElementById('id_blood_form-tube_three').addEventListener('change', function () {
    var style = this.value == 'P' ? 'block' : 'none';
    document.getElementById('tube_three_estimated_volume').style.display = style;
});


$('#id_processed_form-refrigerated_prior_to_processing').click(function() {
  $('#refrigerated_placed_date_time')[this.checked ? "show" : "hide"]();
  $('#refrigerated_removed_date_time')[this.checked ? "show" : "hide"]();
});

document.getElementById('id_processed_form-partial_aliquot_18ml_1_amount').addEventListener('change', function () {
    var style = this.value != '' ? 'block' : 'none';
    document.getElementById('partial_aliquot_18ml_2').style.display = style;
});


// Reload javascript if user hits back button.
$(document).ready(function(e) {
    var $input = $('#refresh');
    $input.val() == 'yes' ? location.reload(true) : $input.val('yes');
});