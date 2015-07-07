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

    //POPOVER util
    $('[data-toggle="popover"]').popover({
        placement : 'bottom',
        container: 'body'
    });

    $('.popoverHoverData').popover();

    $('[data-toggle="popover"]').focusout( function() { $(this).popover("hide") } );

    //DATETIMEPICKER UTIL
    $('.datetimePicker').datetimepicker({
         format: 'YYYY-MM-DD HH:mm:ss',
         toolbarPlacement: 'top',
         showTodayButton: true,
         showClear: true
     });

    //SELECT2 util
    $('select').select2();



    //DATETIMEPICKER util
    //https://github.com/Eonasdan/bootstrap-datetimepicker
});


