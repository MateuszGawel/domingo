from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from main.models import *
import datetime
from django.db.models import Max

def start_duty(request):
    if request.user.is_authenticated():
        duty = None
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

        return render(request, 'main/report_creation.html', {'duty': duty})
    else:
        return render(request, 'main/login.html', None)

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
                return render(request, 'main/report_creation.html', {'error_message': "You have to start your duty first"})
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