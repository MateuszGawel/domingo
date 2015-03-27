from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from main.models import Alert, Comment
import datetime
from django.db.models import Max
from main.forms import *

def add_alert(request):
    report = get_current_report(request)
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
            print "TEST"
            alert.save()
            return __new_alert_form(request)
        else:
            alerts  = Alert.objects.filter(alt_rep_id=report.rep_id)
            return render(request, 'main/report_creation.html', {'form': form, 'alerts': alerts, 'error_message': "Alert has NOT been added"})
    else:
        return __new_alert_form(request)


def __new_alert_form(request, report=None):
    if request.user.is_authenticated():
        if report == None:
            report = get_current_report(request);
        f = AlertForm()
        alerts  = Alert.objects.filter(alt_rep_id=report.rep_id)
        return render(request, 'main/report_creation.html', {'form': f, 'alerts': alerts})
    else:
        return render(request, 'main/login.html', {'error_message': "You have to log in first."})

def create_report(request):
    if Report.objects.filter(rep_usr_id=request.user.id, rep_date_sent=None).exists():
        return redirect('main:index')
    report = Report()
    report.rep_status = 'O'
    report.rep_date_created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report.rep_usr_id = request.user
    report.rep_notes = 'Siema, elo, mowi Spejson'
    report.save()
    return __new_alert_form(request, report)

def edit_report(request):
    report = get_current_report(request)
    return __new_alert_form(request, report)

def close_report(request):
    report = get_current_report(request)
    report.rep_date_sent = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report.rep_status = 'S'
    report.save()
    return redirect('main:index')

def get_current_report(request):
    report = Report.objects.filter(rep_usr_id=request.user.id, rep_date_sent=None).latest('rep_id')
    return report

def browse_reports(request):
    if request.user.is_authenticated():
        f = ReportFilterForm()
        return render(request, 'main/report_browse.html', {'form': f, 'filter_result': None})
    else:
        return render(request, 'main/login.html', {'error_message': "You have to log in first."})

def browse_my_reports(request):
    print "user: " + str(request.user.id)
    if request.user.is_authenticated():
        f = ReportFilterForm()
        f.rep_usr_id = request.user.id
        result = Report.objects.filter(rep_usr_id=request.user.id)
        print result
        return render(request, 'main/report_browse.html', {'form': f, 'filter_result': result})
    else:
        return render(request, 'main/login.html', {'error_message': "You have to log in first."})

def filter_reports(request):
    if request.method == 'POST':
        form = ReportFilterForm(request.POST)
        if form.is_valid():
            filter_result = Report.objects.all()

            if form.cleaned_data.has_key('rep_id') and form.cleaned_data['rep_id'] != "":
                filter_result = filter_result.filter(rep_id=form.cleaned_data['rep_id'])

            if form.cleaned_data.has_key('rep_status') and form.cleaned_data['rep_status'] != "":
                filter_result = filter_result.filter(rep_status=form.cleaned_data['rep_status'])

            if form.cleaned_data.has_key('rep_date_created_from') and form.cleaned_data['rep_date_created_from'] is not None:
                filter_result = filter_result.filter(rep_date_created__gte=form.cleaned_data['rep_date_created_from'])

            if form.cleaned_data.has_key('rep_date_created_to') and form.cleaned_data['rep_date_created_to'] is not None:
                filter_result = filter_result.filter(rep_date_created__lte=form.cleaned_data['rep_date_created_to'])

            if form.cleaned_data.has_key('rep_date_sent_from') and form.cleaned_data['rep_date_sent_from'] is not None:
                filter_result = filter_result.filter(rep_date_sent__gte=form.cleaned_data['rep_date_sent_from'])

            if form.cleaned_data.has_key('rep_date_sent_to') and form.cleaned_data['rep_date_sent_to'] is not None:
                filter_result = filter_result.filter(rep_date_sent__lte=form.cleaned_data['rep_date_sent_to'])

            if form.cleaned_data.has_key('rep_date_removed_from') and form.cleaned_data['rep_date_removed_from'] is not None:
                filter_result = filter_result.filter(rep_date_removed__gte=form.cleaned_data['rep_date_removed_from'])

            if form.cleaned_data.has_key('rep_date_removed_to') and form.cleaned_data['rep_date_removed_to'] is not None:
                filter_result = filter_result.filter(rep_date_removed__lte=form.cleaned_data['rep_date_removed_to'])

            if form.cleaned_data.has_key('rep_usr_id') and form.cleaned_data['rep_usr_id'] != "":
                filter_result = filter_result.filter(rep_usr_id=form.cleaned_data['rep_usr_id'])


            return render(request, 'main/report_browse.html', {'form': form, 'filter_result': filter_result})
        else:
            return render(request, 'main/report_browse.html', {'form': form})
    else:
        return browse_reports(request)
