//Hide component if not clicked
$('#processed_aliquoted_date_time').hide();
$('#refigerated_placed_date_time').hide();
$('#refigerated_removed_date_time').hide();
$('#partial_aliquot_18ml_1').hide();
$('#partial_aliquot_18ml_1_amount').hide();
$('#partial_aliquot_18ml_2').hide();
$('#partial_aliquot_18ml_2_amount').hide();
$('#partial_aliquot_18ml_3').hide();
$('#partial_aliquot_18ml_3_amount').hide();
$('#partial_aliquot_18ml_4').hide();
$('#partial_aliquot_18ml_4_amount').hide();
$('#partial_aliquot_18ml_5').hide();
$('#partial_aliquot_18ml_5_amount').hide();
$('#partial_aliquot_18ml_6').hide();
$('#partial_aliquot_18ml_6_amount').hide();
$('#partial_aliquot_18ml_7').hide();
$('#partial_aliquot_18ml_7_amount').hide();


console.log('reached this')

document.getElementById('id_processed_form-processed_aliquoted_off_site').addEventListener('change', function () {
    var style = this.value == 'R' || this.value=='T' ? 'block' : 'none';
    document.getElementById('processed_aliquoted_date_time').style.display = style;
});

document.getElementById('id_processed_form-all_18_collected').addEventListener('change', function () {
    var style = this.value == 'N'  ? 'block' : 'none';
    document.getElementById('partial_aliquot_18ml_1').style.display = style;
});

$('#id_processed_form-refigerated_prior_to_processing').click(function() {
  $('#refigerated_placed_date_time')[this.checked ? "show" : "hide"]();
  $('#refigerated_removed_date_time')[this.checked ? "show" : "hide"]();
});

$('#id_processed_form-partial_aliquot_18ml_1').click(function() {
  $('#partial_aliquot_18ml_1_amount')[this.checked ? "show" : "hide"]();
});

$('#id_processed_form-partial_aliquot_18ml_2').click(function() {
  $('#partial_aliquot_18ml_2_amount')[this.checked ? "show" : "hide"]();
});

$('#id_processed_form-partial_aliquot_18ml_3').click(function() {
  $('#partial_aliquot_18ml_3_amount')[this.checked ? "show" : "hide"]();
});

$('#id_processed_form-partial_aliquot_18ml_4').click(function() {
  $('#partial_aliquot_18ml_4_amount')[this.checked ? "show" : "hide"]();
});

$('#id_processed_form-partial_aliquot_18ml_5').click(function() {
  $('#partial_aliquot_18ml_5_amount')[this.checked ? "show" : "hide"]();
});

$('#id_processed_form-partial_aliquot_18ml_6').click(function() {
  $('#partial_aliquot_18ml_6_amount')[this.checked ? "show" : "hide"]();
});

$('#id_processed_form-partial_aliquot_18ml_7').click(function() {
  $('#partial_aliquot_18ml_7_amount')[this.checked ? "show" : "hide"]();
});


document.getElementById('id_processed_form-partial_aliquot_18ml_1_amount').addEventListener('change', function () {
    var style = this.value != '' ? 'block' : 'none';
    document.getElementById('partial_aliquot_18ml_2').style.display = style;
});

document.getElementById('id_processed_form-partial_aliquot_18ml_2_amount').addEventListener('change', function () {
    var style = this.value != '' ? 'block' : 'none';
    document.getElementById('partial_aliquot_18ml_3').style.display = style;
});

document.getElementById('id_processed_form-partial_aliquot_18ml_3_amount').addEventListener('change', function () {
    var style = this.value != '' ? 'block' : 'none';
    document.getElementById('partial_aliquot_18ml_4').style.display = style;
});

document.getElementById('id_processed_form-partial_aliquot_18ml_4_amount').addEventListener('change', function () {
    var style = this.value != '' ? 'block' : 'none';
    document.getElementById('partial_aliquot_18ml_5').style.display = style;
});

document.getElementById('id_processed_form-partial_aliquot_18ml_5_amount').addEventListener('change', function () {
    var style = this.value != '' ? 'block' : 'none';
    document.getElementById('partial_aliquot_18ml_6').style.display = style;
});

document.getElementById('id_processed_form-partial_aliquot_18ml_6_amount').addEventListener('change', function () {
    var style = this.value != '' ? 'block' : 'none';
    document.getElementById('partial_aliquot_18ml_7').style.display = style;
});


// Reload javascript if user hits back button.
$(document).ready(function(e) {
    var $input = $('#refresh');
    $input.val() == 'yes' ? location.reload(true) : $input.val('yes');
});