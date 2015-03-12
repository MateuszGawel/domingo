from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from main.models import Alert, Comment
import datetime
from django.db.models import Max
from main.forms import *

def alert_form(request):
    if request.method == 'POST':
            form = AlertForm(request.POST)
            form.is_valid()

            print "VIEW : ", form.cleaned_data

            alert_project = ""
            alert_name = ""
            alert_ticket = ""
            alert_date = ""
            alert_type = ""
            alert_comment = ""

            if form.cleaned_data.has_key('alert_project'):
                alert_project = form.cleaned_data['alert_project']

            if form.cleaned_data.has_key('alert_name'):
                alert_name = form.cleaned_data['alert_name']

            if form.cleaned_data.has_key('alert_ticket'):
                alert_ticket = form.cleaned_data['alert_ticket']

            if form.cleaned_data.has_key('alert_date'):
                alert_date = form.cleaned_data['alert_date']

            if form.cleaned_data.has_key('alert_type'):
                alert_type = form.cleaned_data['alert_type']

            if form.cleaned_data.has_key('alert_comment'):
                alert_comment = form.cleaned_data['alert_comment']

            #TU COS NIE DZIALA
            #comment = Comment()
            #comment.com_value = alert_comment


            #alert = Alert()
            #alert.alt_prj_id = alert_project
            #alert.alt_name = alert_name
            #alert.alt_ticket = alert_ticket
            #alert.alt_date = alert_date
            #alert.alt_type = alert_type
            #alert.alt_com_id = comment.id
            #alert.alt_rep_id = -1

            alert = Alert()
            #alert.alt_prj_id = 1
            alert.alt_name = "aa"
            alert.alt_ticket = "aa"
            #alert.alt_date = "2015-04-05 12:12:12"
            alert.alt_type = "B"
            #alert.alt_com_id = 1
            #alert.alt_rep_id = 1

            #comment.save()
            #alert.save()

            return HttpResponse( "Alert has been added" )
    else:
        return HttpResponse( "Alert is broken. It hasn't been added!" )

def start_duty(request):
    if request.user.is_authenticated():
        duty = None

        f = AlertForm()


        return render(request, 'main/theform.html', {'form': f})
        """
        if not request.session.has_key('duty'):
            global duty
            duty = __check_for_open_duty(request.user.id)
            if duty is None:
                report = Report()
                report.rep_status = 'O'
                report.rep_notes = 'Siema elo jedziemy tutaj'
                report.save()

                global duty
                duty = Duty()
                duty.dut_usr = request.user
                duty.dut_start_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                duty.dut_rep = report
                duty.save()
            request.session['duty'] = duty.dut_id
        else:
            global duty
            duty = get_object_or_404(Duty, dut_id=request.session.get('duty'))

        return render(request, 'main/report.html', {'duty': duty})
    else:
        return render(request, 'main/login.html', None)
    """

def __check_for_open_duty(usr_id):
    duty = Duty.objects.filter(dut_usr_id=usr_id).latest('dut_id')
    if duty is None or duty.dut_end_date is not None:
         return None
    else:
        return duty

def add_alert(request):
    if request.user.is_authenticated():
        duty = None
        if request.session.has_key('duty'):
            global duty
            duty = get_object_or_404(Duty, dut_id=request.session.get('duty'))
        else:
            global duty
            duty = __check_for_open_duty(request.user.id)
            if duty is not None:
                request.session['duty'] = duty.dut_id
            else:
                return render(request, 'main/report.html', {'error_message': "You have to start your duty first"})
        alert = Alert()
        alert.alt_start_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        alert.alt_ticket = request.POST['ticket']
        alert.alt_type = request.POST['type']
        #tu wywala blad bo nie ma jeszcze zadnego projektu
        #alert.alt_prj_id = request.POST['project']
        alert.alt_start_date = request.POST['time']
        alert.alt_rep = duty.dut_rep
        alert.save()
        return HttpResponse(duty)
    else:
        return render(request, 'main/login.html', None)