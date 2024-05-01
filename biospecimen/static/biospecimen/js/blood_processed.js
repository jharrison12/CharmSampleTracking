//Hide component if not clicked
//TODO FIX ALL OF THIS
$('#specimen_received_at_processing_site').hide();
$('#edta_purple_refrigerated_placed_date_time').hide();
$('#edta_purple_refrigerated_removed_date_time').hide();
$('#whole_blood_aliquots_div').hide();
$('#incomplete_blood_spot_card_div').hide();


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

//

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