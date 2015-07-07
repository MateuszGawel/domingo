$(document).ready(function() {

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
        resetSliderValues("#dateSliderCreated");
        resetSliderValues("#dateSliderSent");
        resetSliderValues("#dateSliderAlert");
        resetSliderValues("#dateSliderContact");
        resetSliderValues("#dateSliderMaintenance");
        resetSliderValues("#dateSliderIncidentStart");
        resetSliderValues("#dateSliderIncidentEnd");
        $(this).parent().find("input").each(function ()
        {
            $(this).val("");
        });

    });

    //SLIDER util

    if( document.getElementById("dateSliderCreated") != null )
    {
        $("#dateSliderCreated").dateRangeSlider({
            arrows: false,
            bounds: {min: new Date(2015, 5, 1), max: new Date()},
            defaultValues: {min: new Date(2015, 5, 1), max: new Date()}
        });
        $("#dateSliderCreated").dateRangeSlider({range: {min: {days: 0}}});
        registerEvents("#rep_date_created_from", "#rep_date_created_to", "#dateSliderCreated");
    }

    if( document.getElementById("dateSliderSent") != null )
    {
        $("#dateSliderSent").dateRangeSlider({
            arrows: false,
            bounds: {min: new Date(2015, 5, 1), max: new Date()},
            defaultValues: {min: new Date(2015, 5, 1), max: new Date()}
        });
        $("#dateSliderSent").dateRangeSlider({range: {min: {days: 0}}});
        registerEvents("#rep_date_sent_from", "#rep_date_sent_to", "#dateSliderSent");
    }

    if( document.getElementById("dateSliderAlert") != null )
    {
        $("#dateSliderAlert").dateRangeSlider({
            arrows: false,
            bounds: {min: new Date(2015, 5, 1), max: new Date()},
            defaultValues: {min: new Date(2015, 5, 1), max: new Date()}
        });
        $("#dateSliderAlert").dateRangeSlider({range: {min: {days: 0}}});
        registerEvents("#alt_date_from", "#alt_date_to", "#dateSliderAlert");
    }

    if( document.getElementById("dateSliderContact") != null )
    {
        $("#dateSliderContact").dateRangeSlider({
            arrows: false,
            bounds: {min: new Date(2015, 5, 1), max: new Date()},
            defaultValues: {min: new Date(2015, 5, 1), max: new Date()}
        });
        $("#dateSliderContact").dateRangeSlider({range: {min: {days: 0}}});
        registerEvents("#con_date_from", "#con_date_to", "#dateSliderContact");
    }

    if( document.getElementById("dateSliderMaintenance") != null )
    {
        $("#dateSliderMaintenance").dateRangeSlider({
            arrows: false,
            bounds: {min: new Date(2015, 5, 1), max: new Date()},
            defaultValues: {min: new Date(2015, 5, 1), max: new Date()}
        });
        $("#dateSliderMaintenance").dateRangeSlider({range: {min: {days: 0}}});
        registerEvents("#mnt_date_from", "#mnt_date_to", "#dateSliderMaintenance");
    }

    if( document.getElementById("dateSliderIncidentStart") != null )
    {
        $("#dateSliderIncidentStart").dateRangeSlider({
            arrows: false,
            bounds: {min: new Date(2015, 5, 1), max: new Date()},
            defaultValues: {min: new Date(2015, 5, 1), max: new Date()}
        });
        $("#dateSliderIncidentStart").dateRangeSlider({range: {min: {days: 0}}});
        registerEvents("#inc_date_start_from", "#inc_date_start_to", "#dateSliderIncidentStart");
    }

    if( document.getElementById("dateSliderIncidentEnd") != null )
    {
        $("#dateSliderIncidentEnd").dateRangeSlider({
            arrows: false,
            bounds: {min: new Date(2015, 5, 1), max: new Date()},
            defaultValues: {min: new Date(2015, 5, 1), max: new Date()}
        });
        $("#dateSliderIncidentEnd").dateRangeSlider({range: {min: {days: 0}}});
        registerEvents("#inc_date_end_from", "#inc_date_end_to", "#dateSliderIncidentEnd");
    }


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

        if(fromDate.getTime() <= $(slider).dateRangeSlider("max").getTime() && toDate.getTime() >= $(slider).dateRangeSlider("min").getTime()) {
            $(slider).dateRangeSlider("values", fromDate, toDate);
        }
        else if($(from).val() == "")
            $(slider).dateRangeSlider("values", $(slider).dateRangeSlider("min"), toDate);
        else if($(to).val() == "")
            $(slider).dateRangeSlider("values", fromDate, $(slider).dateRangeSlider("max"));
        else {
            $(slider).dateRangeSlider("values", $(slider).dateRangeSlider("max"), $(slider).dateRangeSlider("min"));
        }
    }

    function resetSliderValues(slider) {
        var from = $(slider).dateRangeSlider("bounds").min;
        var to = $(slider).dateRangeSlider("bounds").max;
        $(slider).dateRangeSlider("values", from, to);
    }
});