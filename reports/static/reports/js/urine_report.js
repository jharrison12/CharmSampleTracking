$('#collected_urine_report').hide();
$('#processed_urine_report').hide();
$('#frozen_urine_report').hide();
$('#shipped_to_wsu_urine_report').hide();
$('#received_at_wsu_urine_report').hide();
$('#shipped_to_echo_urine_report').hide();



$(document).ready(
    document.querySelector('#collected_report_header').addEventListener('click', function(){
        console.log("IS THIS WORKING")
        if ($('#collected_urine_report').is(":hidden")){
              $('#collected_urine_report').show();
            }
        else {
           return $('#collected_urine_report').hide();
        }
}));

$(document).ready(
    document.querySelector('#processed_report_header').addEventListener('click', function(){
        console.log("IS THIS WORKING")
        if ($('#processed_urine_report').is(":hidden")){
              $('#processed_urine_report').show();
            }
        else {
           return $('#processed_urine_report').hide();
        }
}));

$(document).ready(
    document.querySelector('#frozen_report_header').addEventListener('click', function(){
        console.log("IS THIS WORKING")
        if ($('#frozen_urine_report').is(":hidden")){
              $('#frozen_urine_report').show();
            }
        else {
           return $('#frozen_urine_report').hide();
        }
}));

$(document).ready(
    document.querySelector('#shipped_to_wsu_report_header').addEventListener('click', function(){
        console.log("IS THIS WORKING")
        if ($('#shipped_to_wsu_urine_report').is(":hidden")){
              $('#shipped_to_wsu_urine_report').show();
            }
        else {
           return $('#shipped_to_wsu_urine_report').hide();
        }
}));

$(document).ready(
    document.querySelector('#received_at_wsu_report_header').addEventListener('click', function(){
        console.log("IS THIS WORKING")
        if ($('#received_at_wsu_urine_report').is(":hidden")){
              $('#received_at_wsu_urine_report').show();
            }
        else {
           return $('#received_at_wsu_urine_report').hide();
        }
}));


$(document).ready(
    document.querySelector('#shipped_to_echo_report_header').addEventListener('click', function(){
        console.log("IS THIS WORKING")
        if ($('#shipped_to_echo_urine_report').is(":hidden")){
              $('#shipped_to_echo_urine_report').show();
            }
        else {
           return $('#shipped_to_echo_urine_report').hide();
        }
}));


