import datetime
from django.shortcuts import redirect,get_object_or_404
from django.contrib.messages import get_messages
from utils import *
from datetime import date, timedelta
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


            return render(request, 'main/reports/search.html', {'form': form, 'filter_result': filter_result})
        else:
            return render(request, 'main/reports/search.html', {'form': form})
    else:
        return search(request) #?

def create(request):
    if check_csrf(request):

        if Report.objects.filter(rep_usr_id=request.user.id, rep_date_sent=None).exists():
            return redirect("reports:index")
        report = Report()
        report.rep_status = 'O'

        report.rep_date_created = (datetime.datetime.now()- timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        report.rep_usr_id = request.user
        report.rep_notes = 'Siema, elo, mowi Spejson'
        report.save()

        for incident in Incident.objects.filter(inc_status='O'):
            ri = ReportIncident()
            ri.rpi_inc_id = incident
            ri.rpi_rep_id = report
            ri.save()

        return redirect("reports:alert_tab", report.rep_id)

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

def alert_tab(request, rep_id):
    if request.user.is_authenticated():
        report = Report.objects.get(rep_id=rep_id)
        alerts  = Alert.objects.filter(alt_rep_id=report.rep_id)

        if request.method == 'POST':
            form = AlertForm(request.POST)
            if form.is_valid():
                __alert_add(form, report)
                return redirect("reports:alert_tab", report.rep_id)
            else:
                clear_custom_select_data(form.fields['alert_project'])
                add_custom_select_data(form.fields['alert_project'], int(form.cleaned_data['alert_project'])-1, "selected")
                clear_custom_select_data(form.fields['alert_type'])
                add_custom_select_data(form.fields['alert_type'], get_inner_tuple_index(Alert._meta.get_field('alt_type').choices, form.cleaned_data['alert_type'] ), "selected")

        else:
            form = AlertForm()
            clear_custom_select_data(form.fields['alert_project'])
            clear_custom_select_data(form.fields['alert_type'])

        return render(request, 'main/reports/alert_tab.html', {'alertForm': form, 'alerts': alerts, 'report': report})

    else:
        return render(request, 'main/login.html', {'error_message': "You have to log in first."})

def contact_tab(request, rep_id):
    if request.user.is_authenticated():
        report = Report.objects.get(rep_id=rep_id)
        contacts  = Contact.objects.filter(con_rep_id=report.rep_id)

        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                __contact_add(form, report)
                return redirect("reports:contact_tab", report.rep_id)
            else:
                clear_custom_select_data(form.fields['con_prj_id'])
                add_custom_select_data(form.fields['con_prj_id'], int(form.cleaned_data['con_prj_id'])-1, "selected")
                clear_custom_select_data(form.fields['con_type'])
                add_custom_select_data(form.fields['con_type'], get_inner_tuple_index(Contact._meta.get_field('con_type').choices, form.cleaned_data['con_type'] ), "selected")
                clear_custom_select_data(form.fields['con_direction'])
                add_custom_select_data(form.fields['con_direction'], get_inner_tuple_index(Contact._meta.get_field('con_direction').choices, form.cleaned_data['con_direction'] ), "selected")

        else:
            form = ContactForm()
            clear_custom_select_data(form.fields['con_prj_id'])
            clear_custom_select_data(form.fields['con_type'])
            clear_custom_select_data(form.fields['con_direction'])

        return render(request, 'main/reports/contact_tab.html', {'contactForm': form, 'contacts': contacts, 'report': report})

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
            if form.is_valid():
                __incident_add(form, report)
                return redirect("reports:incident_tab", report.rep_id)
            else:
                clear_custom_select_data(form.fields['inc_prj_id'])
                add_custom_select_data(form.fields['inc_prj_id'], int(form.cleaned_data['inc_prj_id'])-1, "selected")
        else:
            form = IncidentForm()
            clear_custom_select_data(form.fields['inc_prj_id'])

        return render(request, 'main/reports/incident_tab.html', {'incidentForm': form, 'incidents': incidents, 'report': report})

    else:
        return render(request, 'main/login.html', {'error_message': "You have to log in first."})

def close(request, rep_id):
    if check_csrf(request):

        report = Report.objects.get(rep_id=rep_id)
        report.rep_date_sent = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report.rep_status = 'S'
        report.save()

    return redirect("reports:index")



#----PRIVATE METHODS----#

def __alert_add(form, report):
    alert = Alert()
    comment = Comment()

    if form.cleaned_data.has_key('alert_project'):
        alert.alt_prj_id = get_object_or_404(Project, prj_id=form.cleaned_data['alert_project'])
    if form.cleaned_data.has_key('alert_name'):
        alert.alt_name = form.cleaned_data['alert_name']
    if form.cleaned_data.has_key('alert_ticket'):
        alert.alt_ticket = form.cleaned_data['alert_ticket']
    if form.cleaned_data.has_key('alert_date'):
        alert.alt_date = form.cleaned_data['alert_date']
    if form.cleaned_data.has_key('alert_type'):
        alert.alt_type = form.cleaned_data['alert_type']
    if form.cleaned_data.has_key('alert_comment'):
        comment.com_value = form.cleaned_data['alert_comment']

    comment.save()

    alert.alt_com_id = comment
    alert.alt_rep_id = report

    alert.save()

def __contact_add(form, report):
    contact = Contact()
    comment = Comment()

    if form.cleaned_data.has_key('con_prj_id'):
        contact.con_prj_id = get_object_or_404(Project, prj_id=form.cleaned_data['con_prj_id'])
    if form.cleaned_data.has_key('con_type'):
        contact.con_type = form.cleaned_data['con_type']
    if form.cleaned_data.has_key('con_address'):
        contact.con_address = form.cleaned_data['con_address']
    if form.cleaned_data.has_key('con_date'):
        contact.con_date = form.cleaned_data['con_date']
    if form.cleaned_data.has_key('con_direction'):
        contact.con_direction = form.cleaned_data['con_direction']
    if form.cleaned_data.has_key('con_internal'):
        contact.con_internal = form.cleaned_data['con_internal']
    if form.cleaned_data.has_key('con_com_id'):
        comment.com_value = form.cleaned_data['con_com_id']

    comment.save()

    contact.con_com_id = comment
    contact.con_rep_id = report

    contact.save()

def __incident_add(form, report):
    incident = Incident()
    comment = Comment()

    if form.cleaned_data.has_key('inc_prj_id'):
        incident.inc_prj_id = get_object_or_404(Project, prj_id=form.cleaned_data['inc_prj_id'])
    if form.cleaned_data.has_key('inc_ticket'):
        incident.inc_ticket = form.cleaned_data['inc_ticket']
    if form.cleaned_data.has_key('inc_date_start'):
        incident.inc_date_start = form.cleaned_data['inc_date_start']
    if form.cleaned_data.has_key('inc_com_id'):
        comment.com_value = form.cleaned_data['inc_com_id']


    comment.save()

    incident.inc_com_id = comment
    incident.inc_status = 'O'
    incident.save()

    reportIncident = ReportIncident()
    reportIncident.rpi_inc_id = incident
    reportIncident.rpi_rep_id = report

    reportIncident.save()