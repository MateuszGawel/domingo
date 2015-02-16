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