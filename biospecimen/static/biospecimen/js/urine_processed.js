//Hide component if not clicked
//TODO FIX ALL OF THIS
$('#processed_aliquoted_date_time').hide();
$('#refrigerated_placed_date_time').hide();
$('#refrigerated_removed_date_time').hide();
$('#partial_aliquot_18ml_volume').hide();
$('#number_of_tubes_collected_18_ml_if_some_missing').hide();
$('#partial_aliquot_7ml_volume').hide();
$('#partial_aliquot_7ml_4_amount').hide();


console.log('reached this')

window.addEventListener("DOMContentLoaded", (event) => {

    const processed_aliquoted_off_site = document.getElementById('id_processed_form-processed_aliquoted_off_site')
    if(processed_aliquoted_off_site){
        processed_aliquoted_off_site.addEventListener('change', function () {
        var style = this.value == 'R' || this.value == 'T' ? 'block' : 'none';
        document.getElementById('processed_aliquoted_date_time').style.display = style;
        });
    }

    const all_18_collected = document.getElementById('id_processed_form-all_18_collected')
    if (all_18_collected){
    all_18_collected.addEventListener('change', function () {
        var style = this.value == "False" ? 'block' : 'none';
        document.getElementById('partial_aliquot_18ml_volume').style.display = style;
        document.getElementById('number_of_tubes_collected_18_ml_if_some_missing').style.display = style;
        });
    };

    const all_7_collected =document.getElementById('id_processed_form-all_7_collected')
    if (all_7_collected){
    all_7_collected.addEventListener('change', function () {
        var style = this.value == "False" ? 'block' : 'none';
        document.getElementById('partial_aliquot_7ml_volume').style.display = style;
        document.getElementById('partial_aliquot_7ml_4_amount').style.display = style;
        });
    }


    $('#id_processed_form-refrigerated_prior_to_processing').click(function () {
        $('#refrigerated_placed_date_time')[this.checked ? "show" : "hide"]();
        $('#refrigerated_removed_date_time')[this.checked ? "show" : "hide"]();
    });

});

// Reload javascript if user hits back button.
$(document).ready(function(e) {
    var $input = $('#refresh');
    $input.val() == 'yes' ? location.reload(true) : $input.val('yes');
});