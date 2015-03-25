from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from main.models import Alert, Comment
import datetime
from django.db.models import Max
from main.forms import *

def add_alert(request):
    report = __get_or_create_empty_Report(request)
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
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

            alert = Alert()
            alert.alt_prj_id = get_object_or_404(Project, prj_id=alert_project)
            alert.alt_name = alert_name
            alert.alt_ticket = alert_ticket
            alert.alt_date = alert_date
            alert.alt_type = alert_type
            comment = Comment()
            comment.com_value = alert_comment
            comment.save()
            alert.alt_com_id = comment
            alert.alt_rep_id = report

            alert.save()

            print "idzie jako dodany"
            return __new_alert(request)
        else:
            alerts  = Alert.objects.filter(alt_rep_id=report.rep_id)
            print "idzie jako zly"
            return render(request, 'main/theform.html', {'form': form, 'alerts': alerts, 'error_message': "Alert has NOT been added"})
    else:
        return __new_alert(request)

def __new_alert(request):
    if request.user.is_authenticated():
        report = __get_or_create_empty_Report(request);
        f = AlertForm()
        alerts  = Alert.objects.filter(alt_rep_id=report.rep_id)
        return render(request, 'main/theform.html', {'form': f, 'alerts': alerts})
    else:
        return render(request, 'main/login.html', {'error_message': "You have to log in first."})

def __get_or_create_empty_Report(request):
    report = None
    if request.session.has_key('report'):
        global report
        report = get_object_or_404(Report, rep_id=request.session.get('report'))
    else:
        global report
        report = Report.objects.filter(rep_usr_id=request.user.id).latest('rep_id')

    if report is None or report.rep_date_sent is not None:
        global report
        report = Report()
        report.rep_status = 'O'
        report.rep_date_created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report.rep_usr_id = request.user
        report.rep_notes = 'Siema, elo, mowi Spejson'
        report.save()
        request.session['report'] = report.rep_id
    else:
        global report
        request.session['report'] = report.rep_id
    return report