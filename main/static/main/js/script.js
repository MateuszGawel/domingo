$(document).ready(function() {

    //AJAX util
    $('.add-alert-form').submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: $(this).attr("action"),
            data: $(this).serialize(),

            success: function (data) {
                $("#alerts").load(" #alerts");
            }
        });
    });

    //DISABLE DISABLED FORMS
    $('.disabled-form').submit(function (e) {
        e.preventDefault();
    });

    //CLEAR FOR GET util
    $(".get-clear").submit(function(e){

            $(this).find("input").each(function () {
                if ($(this).val() == '') {
                    this.setAttribute("name", "");
                }
            });
    });

    //CLEAR FOR GET util
    $("form").find(".clear").click(function(e){
            e.preventDefault();
            $(this).parent().find("input").each(function ()
            {
                $(this).val("");
            });
    });

    //POPOVER util
    $('[data-toggle="popover"]').popover({
        placement : 'bottom',
        container: 'body'
    });

    $('[data-toggle="popover"]').focusout( function() { $(this).popover("hide") } );

    //SELECT2 util
    //$('select').select2();

    //SLIDER util
    $("#dateSliderCreated").dateRangeSlider({arrows:false, bounds:{ min: new Date(2013, 4, 1), max: new Date()},   defaultValues:{ min: new Date(2013, 4, 1), max: new Date()} });
    $("#dateSliderSent").dateRangeSlider({arrows:false, bounds:{ min: new Date(2015, 4, 1), max: new Date()},   defaultValues:{ min: new Date(2015, 4, 1), max: new Date()} });
    $("#dateSliderRemoved").dateRangeSlider({arrows:false, bounds:{ min: new Date(2015, 4, 1), max: new Date()},   defaultValues:{ min: new Date(2015, 4, 1), max: new Date()} });

    $("#dateSliderCreated").bind("valuesChanged", function(e, data){
        $("#id_rep_date_created_from").val(moment( $("#dateSliderCreated").dateRangeSlider("min")).format('YYYY-MM-DD 00:00:00'));
        $("#id_rep_date_created_to").val(moment( $("#dateSliderCreated").dateRangeSlider("max")).format('YYYY-MM-DD 00:00:00'));
      console.log("Values just changed. min: " + data.values.min + " max: " + data.values.max);
    });
});

//DATETIMEPICKER util
//https://github.com/Eonasdan/bootstrap-datetimepicker
$(function () {
    $('.datetimePicker').datetimepicker({
        format: 'YYYY-MM-DD HH:mm:ss',
        toolbarPlacement: 'top',
        showTodayButton: true,
        showClear: true
    });
});
