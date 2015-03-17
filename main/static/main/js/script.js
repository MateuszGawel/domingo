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

    //POPOVER util
    $('[data-toggle="popover"]').popover({
        placement : 'right',
        container: 'body'
    });

    //SELECT2 util
    $('select').select2();
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
