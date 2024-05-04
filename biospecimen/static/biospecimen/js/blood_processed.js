//Hide component if not clicked
//TODO FIX ALL OF THIS
$('#specimen_received_at_processing_site').hide();
$('#edta_purple_refrigerated_placed_date_time').hide();
$('#edta_purple_refrigerated_removed_date_time').hide();
$('#whole_blood_aliquots_div').hide();
$('#incomplete_blood_spot_card_div').hide();
$('#plasma_purple_cap_200_microliter_number_collected').hide();
$('#plasma_purple_cap_1_ml_partial_aliquots').hide();
$('#buffy_coat_partial_aliquots').hide();
$('#red_blood_cells_partial_aliquots').hide();
$('#serum_red_cap_200_microl_number_aliquots_collected').hide();
$('#serum_red_cap_1_ml_partial_aliquots').hide();


console.log('reached this')

document.getElementById('id_processed_form-edta_purple_tube_refrigerated_prior_to_centrifuge').addEventListener('change', function () {
    var style = this.value == 'True' ? 'block' : 'none';
    document.getElementById('edta_purple_refrigerated_placed_date_time').style.display = style;
    document.getElementById('edta_purple_refrigerated_removed_date_time').style.display = style;
});

// id_processed_form-blood_spot_card_completed

document.getElementById('id_processed_form-blood_spot_card_completed').addEventListener('change', function () {
    var style = this.value == 'False' ? 'block' : 'none';
    document.getElementById('incomplete_blood_spot_card_div').style.display = style;
});

document.getElementById('id_processed_form-whole_blood_blue_cap_collected').addEventListener('change', function () {
    var style = this.value == 'False' ? 'block' : 'none';
    document.getElementById('whole_blood_aliquots_div').style.display = style;
});

document.getElementById('id_processed_form-plasma_purple_cap_200_microliter_all_collected').addEventListener('change', function () {
    var style = this.value == 'False' ? 'block' : 'none';
    document.getElementById('plasma_purple_cap_200_microliter_number_collected').style.display = style;
});

document.getElementById('id_processed_form-plasma_purple_cap_1_ml_all_collected').addEventListener('change', function () {
    var style = this.value == 'False' ? 'block' : 'none';
    document.getElementById('plasma_purple_cap_1_ml_partial_aliquots').style.display = style;
});

document.getElementById('id_processed_form-buffy_coat_green_cap_1_ml_all_collected').addEventListener('change', function () {
    var style = this.value == 'False' ? 'block' : 'none';
    document.getElementById('buffy_coat_partial_aliquots').style.display = style;
});

document.getElementById('id_processed_form-red_blood_cells_yellow_cap_1_ml_all_collected').addEventListener('change', function () {
    var style = this.value == 'False' ? 'block' : 'none';
    document.getElementById('red_blood_cells_partial_aliquots').style.display = style;
});


document.getElementById('id_processed_form-serum_red_cap_200_microl_all_collected').addEventListener('change', function () {
    var style = this.value == 'False' ? 'block' : 'none';
    document.getElementById('serum_red_cap_200_microl_number_aliquots_collected').style.display = style;
});


document.getElementById('id_processed_form-serum_red_cap_1_ml_all_collected').addEventListener('change', function () {
    var style = this.value == 'False' ? 'block' : 'none';
    document.getElementById('serum_red_cap_1_ml_partial_aliquots').style.display = style;
});

//

$('#id_processed_form-refrigerated_prior_to_processing').click(function() {
  $('#refrigerated_placed_date_time')[this.checked ? "show" : "hide"]();
  $('#refrigerated_removed_date_time')[this.checked ? "show" : "hide"]();
});


// Reload javascript if user hits back button.
$(document).ready(function(e) {
    var $input = $('#refresh');
    $input.val() == 'yes' ? location.reload(true) : $input.val('yes');
});