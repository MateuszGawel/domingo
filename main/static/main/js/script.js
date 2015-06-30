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

    //POPOVER util
    $('[data-toggle="popover"]').popover({
        placement : 'bottom',
        container: 'body'
    });

    $('[data-toggle="popover"]').focusout( function() { $(this).popover("hide") } );

    //SELECT2 util
    //$('select').select2();



    //DATETIMEPICKER util
    //https://github.com/Eonasdan/bootstrap-datetimepicker
});


