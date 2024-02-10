// $('#collected_urine_report').hide();



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
