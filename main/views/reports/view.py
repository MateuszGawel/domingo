import datetime
from datetime import timedelta
from django.shortcuts import redirect, render
from utils import *


def index(request):
    if request.user.is_authenticated():
        report = Report.objects.filter(rep_usr_id=request.user.id)
        if report.exists():
            report = report.latest('rep_id')
        else:
            report = None
        return render(request, 'main/reports/index.html', {'report': report, 'user': request.user})
    else:
        return render(request, 'main/login.html', None)

def search(request):
    if request.method == 'GET':
        form = ReportFilterForm(request.GET)
        if doValidate(form):
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


            return render(request, 'main/reports/search.html', {'form': form, 'filter_result': filter_result})
        else:
            return render(request, 'main/reports/search.html', {'form': form})
    else:
        return search(request) #?

def create(request):
    if request.method == 'POST':
        if doValidate(form=forms.Form(request.POST)):

            if Report.objects.filter(rep_usr_id=request.user.id, rep_date_sent=None).exists():
                return redirect("reports:index")
            report = Report()
            report.rep_status = 'O'

            report.rep_date_created = (datetime.datetime.now()- timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
            report.rep_usr_id = request.user
            comment = Comment()
            comment.com_value = ''
            comment.save()
            report.rep_com_id = comment
            report.save()

            for incident in Incident.objects.filter(inc_status='O'):
                ri = ReportIncident()
                ri.rpi_inc_id = incident
                ri.rpi_rep_id = report
                ri.save()

            return redirect("reports:summary_tab", report.rep_id)

    return redirect("reports:index")

def get_alerts_from_jira(request, rep_id):
    if request.user.is_authenticated():
        report = Report.objects.get(rep_id=rep_id)
        query = " select project.pname, jiraissue.summary, jiraissue.pkey, jiraissue.created from jiraissue, project where jiraissue.reporter = '" + request.user.username + "' and jiraissue.created >= to_date('" + report.rep_date_created.strftime('%Y-%m-%d %H:%M:%S') +"', 'yyyy-mm-dd hh24:mi:ss') and jiraissue.created <= sysdate and project.id = jiraissue.project"

        for record in get_data_from_jira(query).fetchall():
            project = Project.objects.get(prj_name = record[0])
            ticket = "https://loyaltysupport.comarch.pl/browse/" + record[2]

            if Alert.objects.filter(alt_ticket = ticket, alt_rep_id = rep_id).count() > 0:
                continue

            alert = Alert()
            alert.alt_prj_id = project
            alert.alt_name = record[1]
            alert.alt_ticket = ticket
            alert.alt_date = record[3]

            alert.alt_rep_id = report
            alert.alt_type = 'B'

            comment = Comment()
            comment.save()
            alert.alt_com_id = comment

            alert.save()

        return redirect("reports:alert_tab", report.rep_id)
    else:
        return render(request, 'main/login.html', {'error_message': "You have to log in first."})

def summary_tab(request, rep_id):
    if request.user.is_authenticated():
        report = Report.objects.get(rep_id=rep_id)

        if request.method == 'POST':
            form = SummaryForm(request.POST)
            if doValidate(form, request, report):
                form.save(report)
                return redirect("reports:summary_tab", report.rep_id)

            else:
                pass

        else:
            rep_redirection = ""
            if report.rep_redirection is not None:
                rep_redirection = str(report.rep_redirection)
            form = SummaryForm({'rep_redirection': rep_redirection, 'rep_comment': report.rep_com_id.com_value})
        return render(request, 'main/reports/summary_tab.html', {'summaryForm': form, 'report': report})

    else:
        return render(request, 'main/login.html', {'error_message': "You have to log in first."})

def find_report(request, inc_id):
    report = None

    reportIncident = ReportIncident.objects.filter(rpi_inc_id = inc_id)

    for ri in reportIncident:
        report = Report.objects.get(rep_id = ri.rpi_rep_id.rep_id)
        if report.rep_status == 'O' and report.rep_usr_id == request.user:
            break

    return report

def alert_tab(request, rep_id=None, inc_id=None):
    if request.user.is_authenticated():
        report = None
        if rep_id == None:
            report = find_report(request, inc_id)
        else:
            report = Report.objects.get(rep_id=rep_id)

        alerts  = Alert.objects.filter(alt_rep_id=report.rep_id)
        filledAlertForms = []
        for alert in alerts:
            filledAlertform = AlertForm({'alert_project': alert.alt_prj_id.prj_id,
                                   'alert_name': alert.alt_name,
                                   'alert_ticket': alert.alt_ticket,
                                   'alert_date': str( alert.alt_date ),
                                   'alert_type': alert.alt_type,
                                   'alert_comment': alert.alt_com_id.com_value})
            filledAlertForms.append( (alert, filledAlertform) )

        if request.method == 'POST':
            form = AlertForm(request.POST)
            if doValidate(form, request, report):
                if inc_id == None:
                    form.save(report)
                    return redirect("reports:alert_tab", report.rep_id)
                else:
                    form.save(report, inc_id)
                    return redirect("incidents:details", report.rep_id, inc_id)

        else:
            form = AlertForm()
        return render(request, 'main/reports/alert_tab.html', {'alertForm': form, 'alerts': filledAlertForms, 'report': report, 'inc_id': inc_id})

    else:
        return render(request, 'main/login.html', {'error_message': "You have to log in first."})

def contact_tab(request, rep_id=None, inc_id=None):
    if request.user.is_authenticated():
        report = None
        if rep_id == None:
            report = find_report(request, inc_id)
        else:
            report = Report.objects.get(rep_id=rep_id)

        contacts  = Contact.objects.filter(con_rep_id=report.rep_id)
        filledContactForms = []
        for contact in contacts:
            filledContactform = ContactForm({'con_prj_id': contact.con_prj_id.prj_id,
                                   'con_type': contact.con_type,
                                   'con_address': contact.con_address,
                                   'con_date': str( contact.con_date ),
                                   'con_direction': contact.con_direction,
                                   'con_internal': contact.con_internal,
                                   'con_com_id': contact.con_com_id.com_value})
            filledContactForms.append( (contact, filledContactform) )

        if request.method == 'POST':
            form = ContactForm(request.POST)
            if doValidate(form, request, report):
                if inc_id == None:
                    form.save(report)
                    return redirect("reports:contact_tab", report.rep_id)
                else:
                    form.save(report, inc_id)
                    return redirect("incidents:details", report.rep_id, inc_id)

        else:
            form = ContactForm()

        return render(request, 'main/reports/contact_tab.html', {'contactForm': form, 'contacts': filledContactForms, 'report': report, 'inc_id': inc_id})

    else:
        return render(request, 'main/login.html', {'error_message': "You have to log in first."})

def maintenance_tab(request, rep_id=None, inc_id=None):
    if request.user.is_authenticated():

        report = None
        if rep_id == None:
            report = find_report(request, inc_id)
        else:
            report = Report.objects.get(rep_id=rep_id)

        maintenances  = Maintenance.objects.filter(mnt_rep_id=report.rep_id)
        filledMaintenanceForms = []
        for maintenance in maintenances:
            filledMaintenanceForm = MaintenanceForm({'mnt_prj_id': maintenance.mnt_prj_id.prj_id,
                                    'mnt_name': maintenance.mnt_name,
                                    'mnt_date': str( maintenance.mnt_date ),
                                    'mnt_com_id': maintenance.mnt_com_id.com_value,
            })
            filledMaintenanceForms.append( (maintenance, filledMaintenanceForm) )

        if request.method == 'POST':
            form = MaintenanceForm(request.POST)
            if doValidate(form, request, report):
                if inc_id == None:
                    form.save( report)
                    return redirect("reports:maintenance_tab", report.rep_id)
                else:
                    form.save( report, inc_id)
                    return redirect("incidents:details", report.rep_id, inc_id)
        else:
            form = MaintenanceForm()

        return render(request, 'main/reports/maintenance_tab.html', {'maintenances': filledMaintenanceForms, 'maintenanceForm' : form, 'report': report, 'inc_id': inc_id})

    else:
        return render(request, 'main/login.html', {'error_message': "You have to log in first."})

def incident_tab(request, rep_id):
    if request.user.is_authenticated():
        report = Report.objects.get(rep_id=rep_id)

        incidents = []

        for ri in ReportIncident.objects.filter(rpi_rep_id = rep_id):
            incidents.append( ri.rpi_inc_id )

        if request.method == 'POST':
            form = IncidentForm(request.POST)
            if doValidate(form, request, report):
                form.save( report)
                return redirect("reports:incident_tab", report.rep_id)
        else:
            form = IncidentForm()

        return render(request, 'main/reports/incident_tab.html', {'incidentForm': form, 'incidents': incidents, 'report': report})

    else:
        return render(request, 'main/login.html', {'error_message': "You have to log in first."})

def close(request, rep_id):
    report = Report.objects.get(rep_id=rep_id)

    if request.method == 'POST':
        if doValidate(form=forms.Form(request.POST), request=request, report=report):

            report.rep_date_sent = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            report.rep_status = 'C'
            report.save()

    return redirect("reports:index")

def incident_alert_tab(request, rep_id, inc_id):
    return alert_tab(request, rep_id, inc_id)

def incident_contact_tab(request, rep_id, inc_id):
    return contact_tab(request, rep_id, inc_id)

def incident_maintenance_tab(request, rep_id, inc_id):
    return maintenance_tab(request, rep_id, inc_id)