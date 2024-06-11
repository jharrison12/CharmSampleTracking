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
$('#tube_1_estimated_volume').hide();
$('#tube_2_estimated_volume').hide();
$('#tube_3_estimated_volume').hide();

console.log('reached this')

window.addEventListener("DOMContentLoaded", (event) => {

    const edta_purple_tube_refrigerated_prior_to_centrifuge = document.getElementById('id_processed_form-edta_purple_tube_refrigerated_prior_to_centrifuge');
    if (edta_purple_tube_refrigerated_prior_to_centrifuge) {
        edta_purple_tube_refrigerated_prior_to_centrifuge.addEventListener('change', function () {
            var style = this.value == 'True' ? 'block' : 'none';
            document.getElementById('edta_purple_refrigerated_placed_date_time').style.display = style;
            document.getElementById('edta_purple_refrigerated_removed_date_time').style.display = style;
            $('#id_processed_form-edta_purple_refrigerated_placed_date_time').val('');
            $('#id_processed_form-edta_purple_refrigerated_removed_date_time').val('');
            // document.getElementById('edta_purple_refrigerated_removed_date_time').textContent='';
        })
    }
    ;


    const processed_aliquoted_off_site = document.getElementById('id_processed_form-processed_aliquoted_off_site')
    if (processed_aliquoted_off_site) {
        processed_aliquoted_off_site.addEventListener('change', function () {
            var style = this.value != 'N' ? 'block' : 'none';
            document.getElementById('specimen_received_at_processing_site').style.display = style;

        })
    };

    const blood_spot_card_completed = document.getElementById('id_processed_form-blood_spot_card_completed')
    if (blood_spot_card_completed){
        blood_spot_card_completed.addEventListener('change', function () {
            var style = this.value == 'False' ? 'block' : 'none';
            document.getElementById('incomplete_blood_spot_card_div').style.display = style;
            $('#id_processed_form-blood_spot_card_number_of_complete_spots').val('');
            $('#id_processed_form-blood_spot_card_number_of_dots_smaller_than_dotted_circle').val('');
            $('#id_processed_form-blood_spot_card_number_of_dotted_circle_missing_blood_spot').val('');

        })
    };

    const whole_blood_blue_cap_all_collected = document.getElementById('id_processed_form-whole_blood_blue_cap_all_collected')
    if (whole_blood_blue_cap_all_collected){
        whole_blood_blue_cap_all_collected.addEventListener('change', function () {
        var style = this.value == 'False' ? 'block' : 'none';
        document.getElementById('whole_blood_aliquots_div').style.display = style;
        $('#id_processed_form-whole_blood_blue_cap_partial_aliquot_volume').val('');
        $('#id_processed_form-whole_blood_blue_cap_number_collected').val('');
        })
    };

    const plasma_purple_cap_200_microliter_all_collected = document.getElementById('id_processed_form-plasma_purple_cap_200_microliter_all_collected')
    if (plasma_purple_cap_200_microliter_all_collected){
        plasma_purple_cap_200_microliter_all_collected.addEventListener('change', function () {
        var style = this.value == 'False' ? 'block' : 'none';
        document.getElementById('plasma_purple_cap_200_microliter_number_collected').style.display = style;
        })
    };

    const plasma_purple_cap_1_ml_all_collected = document.getElementById('id_processed_form-plasma_purple_cap_1_ml_all_collected')
    if (plasma_purple_cap_1_ml_all_collected){
        plasma_purple_cap_1_ml_all_collected.addEventListener('change', function () {
        var style = this.value == 'False' ? 'block' : 'none';
        document.getElementById('plasma_purple_cap_1_ml_partial_aliquots').style.display = style;
        })
    };

    const buffy_coat_green_cap_1_ml_all_collected = document.getElementById('id_processed_form-buffy_coat_green_cap_1_ml_all_collected');
    if (buffy_coat_green_cap_1_ml_all_collected) {
            buffy_coat_green_cap_1_ml_all_collected.addEventListener('change', function () {
            var style = this.value == 'False' ? 'block' : 'none';
            document.getElementById('buffy_coat_partial_aliquots').style.display = style;
        })
    };

    const red_blood_cells_yellow_cap_1_ml_all_collected = document.getElementById('id_processed_form-red_blood_cells_yellow_cap_1_ml_all_collected')
    if (red_blood_cells_yellow_cap_1_ml_all_collected){
            red_blood_cells_yellow_cap_1_ml_all_collected.addEventListener('change', function () {
            var style = this.value == 'False' ? 'block' : 'none';
            document.getElementById('red_blood_cells_partial_aliquots').style.display = style;
        })
    };

    const serum_red_cap_200_microl_all_collected = document.getElementById('id_processed_form-serum_red_cap_200_microl_all_collected')
        if (serum_red_cap_200_microl_all_collected){
            serum_red_cap_200_microl_all_collected.addEventListener('change', function () {
            var style = this.value == 'False' ? 'block' : 'none';
            document.getElementById('serum_red_cap_200_microl_number_aliquots_collected').style.display = style;
        })
    };

    const serum_red_cap_1_ml_all_collected = document.getElementById('id_processed_form-serum_red_cap_1_ml_all_collected')
    if (serum_red_cap_1_ml_all_collected){
        serum_red_cap_1_ml_all_collected.addEventListener('change', function () {
        var style = this.value == 'False' ? 'block' : 'none';
        document.getElementById('serum_red_cap_1_ml_partial_aliquots').style.display = style;
        })
    };

    const refrigerated_prior_to_processing = document.getElementById('id_processed_form-refrigerated_prior_to_processing')
    if (refrigerated_prior_to_processing){
        refrigerated_prior_to_processing.click(function () {
        $('#refrigerated_placed_date_time')[this.checked ? "show" : "hide"]();
        $('#refrigerated_removed_date_time')[this.checked ? "show" : "hide"]();
        })
    };


    const tube_1 = document.getElementById('id_blood_form-tube_1')
    if (tube_1){
            tube_1.addEventListener('change', function () {
            var style = this.value == 'P' ? 'block' : 'none';
            document.getElementById('tube_1_estimated_volume').style.display = style;
            $('#id_blood_form-tube_1_estimated_volume').val('');
        })
    };


    const tube_2 = document.getElementById('id_blood_form-tube_2')
        if(tube_2){
            tube_2.addEventListener('change', function () {
            var style = this.value == 'P' ? 'block' : 'none';
            document.getElementById('tube_2_estimated_volume').style.display = style;
            $('#id_blood_form-tube_2_estimated_volume').val('');
        })
    };

    const tube_3 = document.getElementById('id_blood_form-tube_3')
        if (tube_3){
            tube_3.addEventListener('change', function () {
            var style = this.value == 'P' ? 'block' : 'none';
            document.getElementById('tube_3_estimated_volume').style.display = style;
            $('#id_blood_form-tube_3_estimated_volume').val('');
        })
    }
;

    const partial_aliquot_18ml_1_amount =document.getElementById('id_processed_form-partial_aliquot_18ml_1_amount')
        if (partial_aliquot_18ml_1_amount){
            partial_aliquot_18ml_1_amount.addEventListener('change', function () {
            var style = this.value != '' ? 'block' : 'none';
            document.getElementById('partial_aliquot_18ml_2').style.display = style;
        })
    }
;


});

// Reload javascript if user hits back button.
$(document).ready(function(e) {
    var $input = $('#refresh');
    $input.val() == 'yes' ? location.reload(true) : $input.val('yes');
});