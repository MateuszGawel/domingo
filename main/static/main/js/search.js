$(document).ready(function() {
    //SLIDER util
    $("#dateSliderCreated").dateRangeSlider({arrows:false, bounds:{ min: new Date(2015, 0, 1), max: new Date()},   defaultValues:{ min: new Date(2015, 0, 1), max: new Date()} });
    $("#dateSliderCreated").dateRangeSlider({range:{min: {days: 0}}});
    registerEvents("#rep_date_created_from", "#rep_date_created_to","#dateSliderCreated");

    $("#dateSliderSent").dateRangeSlider({arrows:false, bounds:{ min: new Date(2015, 0, 1), max: new Date()},   defaultValues:{ min: new Date(2015, 0, 1), max: new Date()} });
    $("#dateSliderSent").dateRangeSlider({range:{min: {days: 0}}});
    registerEvents("#rep_date_sent_from", "#rep_date_sent_to","#dateSliderSent");

    $("#dateSliderRemoved").dateRangeSlider({arrows:false, bounds:{ min: new Date(2015, 0, 1), max: new Date()},   defaultValues:{ min: new Date(2015, 0, 1), max: new Date()} });
    $("#dateSliderRemoved").dateRangeSlider({range:{min: {days: 0}}});
    registerEvents("#rep_date_removed_from", "#rep_date_removed_to","#dateSliderRemoved");


    function registerEvents(from, to, slider){
        $(slider).bind("valuesChanged", function(e, data){
            if($(slider).dateRangeSlider("bounds").min.getTime() != $(slider).dateRangeSlider("min").getTime())
                $(from).val(moment( $(slider).dateRangeSlider("min")).format('YYYY-MM-DD'));
            else
                $(from).val("");
            if($(slider).dateRangeSlider("bounds").max.getTime() != $(slider).dateRangeSlider("max").getTime())
                $(to).val(moment( $(slider).dateRangeSlider("max")).format('YYYY-MM-DD'));
            else
                $(to).val("");
        });
        if( $(from).val() != "" ){
            setSliderValues(from, to, slider);
        }
        if( $(to).val() != "" ){
            setSliderValues(from, to, slider);
        }

        $(function () {
            $(from).parent().datetimepicker({
                format: 'YYYY-MM-DD',
                toolbarPlacement: 'top',
                showTodayButton: true,
                showClear: true
            }).on('dp.change', function(ev){
                    setSliderValues(from, to, slider);
                  });
        });
        $(function () {
            $(to).parent().datetimepicker({
                format: 'YYYY-MM-DD',
                toolbarPlacement: 'top',
                showTodayButton: true,
                showClear: true
            }).on('dp.change', function(ev){
                    setSliderValues(from, to, slider);
                  });
        });
    }

    function setSliderValues(from, to, slider) {
        var date = $(from).val();
        var res = date.split("-", 3);
        var fromDate = new Date(parseInt(res[0]),parseInt(res[1])-1,parseInt(res[2]));
        date = $(to).val();
        res = date.split("-", 3);
        var toDate = new Date(parseInt(res[0]),parseInt(res[1])-1,parseInt(res[2]));

        if(fromDate.getTime() <= $("#dateSliderCreated").dateRangeSlider("max").getTime() && toDate.getTime() >= $("#dateSliderCreated").dateRangeSlider("min").getTime()) {
            $(slider).dateRangeSlider("values", fromDate, toDate);
        }
        else if($(from).val() == "")
            $(slider).dateRangeSlider("values", $("#dateSliderCreated").dateRangeSlider("min"), toDate);
        else if($(to).val() == "")
            $(slider).dateRangeSlider("values", fromDate, $("#dateSliderCreated").dateRangeSlider("max"));
        else {
            $(slider).dateRangeSlider("values", $("#dateSliderCreated").dateRangeSlider("max"), $("#dateSliderCreated").dateRangeSlider("min"));
        }
    }

    function resetSliderValues(slider) {
        var from = $("#dateSliderCreated").dateRangeSlider("bounds").min;
        var to = $("#dateSliderCreated").dateRangeSlider("bounds").max;
        $(slider).dateRangeSlider("values", from, to);
    }
});