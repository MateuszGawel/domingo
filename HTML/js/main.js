// ==================   start tab.js   script ===============
$(document).ready(function(){
	$("#tabs li a").each(function (i) {
		$("#tabs li:eq("+i+")").click(function(){
			var tab_id=i+1;
			$("#tabs li").removeClass("active");
			$(this).addClass("active");
			$(".tab-content > div").removeClass("active");
			$("#tab"+tab_id).addClass("active");
			$(".tab-content > div").stop(false,false).hide();
			$("#tab"+tab_id).stop(false,false).show();
			return false;
		})
	})
})

// =====================   END  tab.js   BEGIN calendar ============

$(document).ready(function() {

var date = new Date();
  var d = date.getDate();
  var m = date.getMonth();
  var y = date.getFullYear();

  
  $('#calendar').fullCalendar({

    header: {
      left: 'prev,next today',
      center: 'title',
      right: 'month,agendaWeek,agendaDay'
    },
    editable: true,
    events: [
      {
        title: 'All Day Event',
        start: new Date(y, m, 1)
      },
      {
        title: 'Long Event',
        start: new Date(y, m, d-5),
        end: new Date(y, m, d-2)
      },
      {
        id: 999,
        title: 'Repeating Event',
        start: new Date(y, m, d-3, 16, 0),
        allDay: false
      },
      {
        id: 999,
        title: 'Repeating Event',
        start: new Date(y, m, d+4, 16, 0),
        allDay: false
      },
      {
        title: 'Meeting',
        start: new Date(y, m, d, 10, 30),
        allDay: false
      },
      {
        title: 'Lunch',
        start: new Date(y, m, d, 12, 0),
        end: new Date(y, m, d, 14, 0),
        allDay: false
      },
      {
        title: 'Birthday Party',
        start: new Date(y, m, d+1, 19, 0),
        end: new Date(y, m, d+1, 22, 30),
        allDay: false
      },
      {
        title: 'Click for Google',
        start: new Date(y, m, 28),
        end: new Date(y, m, 29),
        url: 'http://google.com/'
      }
    ]
  });
})

// ====================  END calendar ===================

//  ===================  Select.js ======================
$(document).ready(function() {              
  $('.selectpicker').selectpicker({
    style: 'btn',
    size: 4
  });
});   

//  ====================  Dialog window ==============


 $("#myModal").on("show", function() { // wire up the OK button to dismiss the modal when shown
$("#myModal a.btn").on("click", function(e) {
console.log("button pressed"); // just as an example...
$("#myModal").modal('hide'); // dismiss the dialog
});
});
$("#myModal").on("hide", function() { // remove the event listeners when the dialog is dismissed
$("#myModal a.btn").off("click");
});
$("#myModal").on("hidden", function() { // remove the actual elements from the DOM when fully hidden
$("#myModal").remove();
});
$("#myModal").modal({ // wire up the actual modal functionality and show the dialog
"backdrop" : "static",
"keyboard" : true,
"show" : true // ensure the modal is shown immediately
}); 

        //  ========== dialog body ==============

bootbox.dialog({
title: "Details of the incident",
message:    '<div class="row"> ' +
                '<div class="date_text col-md-12"> ' +
                  '<label class="col-md-6 control-label" for="name">Project</label> ' +
                  '<div class="col-md-6"> ALMA </div> ' +
                '</div>'+
                '<div class="date_text col-md-12"> ' +
                  '<label class="col-md-6 control-label" for="name">Ticket</label> ' +
                  '<div class="col-md-6"> ALMA-345 </div> ' +
                '</div>'+
                '<div class="date_text col-md-12"> ' +
                  '<label class="col-md-6 control-label" for="name">Data of start incident</label> ' +
                  '<div class="col-md-6"> 2015-03-01 00:01 </div> ' +
                '</div>'+
                '<div class="date_text col-md-12"> ' +
                  '<label class="col-md-6 control-label" for="name">Data of end incident</label> ' +
                  '<div class="col-md-6"> 2015-03-01 00:01 </div> ' +
                '</div>'+
                '<div class="btns">'+
                  '<a class="btn btn-danger edit_btn bootbox-close-button" href="javascript:void(0)">Close</a>'+
                  '<a class="btn btn-primary edit_btn" href="javascript:void(0)">Edit</a>'+
                '</div>' +
            '</div>'+
            //  Step 1
            '<hr></hr>'+
            '<form class="form-horizontal well"> ' +
              '<fildset>'+
                '<legend> Step 1</legend>'+
                '<div class="form-group .resp_group"> ' + 
                      '<select class="selectpicker" multiple title="select" data-width="140px">'+
                        '<option>qwerty</option>'+
                        '<option>ytrewq</option>'+
                        '<option>qazxswedc</option>'+
                      '</select>'+
                '</div>'+
                '<div class="form-group .resp_group"> ' + 
                  '<textarea id="textarea" class="form-control input-xlarge" rows="3"></textarea>'+
                '</div>'+
                '<div class="form-group"> ' + 
                  '<div class="btns">'+
                    '<button class="btn btn-success edit_btn" type="submit">Save</button>'+
                    '<a class="btn btn-primary edit_btn" href="javascript:void(0)">Next step</a>'+
                  '</div>' +
                '</div>'+
              '</fildset>'+
            '</form>'
}
); 