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

    //SELECT2 util
    //$('select').select2();
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
