import datetime

from django.shortcuts import get_object_or_404, redirect, render
from django.forms import Form

from main.views.reports.utils import *


class Entity:

    def __init__(self, name, date, type, url, ins_id, id):
        self.ent_number = 0
        self.ent_name = name
        self.ent_date = date
        self.ent_type = type

        self.ent_url = url
        self.ent_ins_id = ins_id
        self.ent_id = id


def details(request, rep_id, inc_id):

    reportIncident = ReportIncident.objects.filter(rpi_inc_id = inc_id)

    report = None

    for ri in reportIncident:
        report = Report.objects.get(rep_id = ri.rpi_rep_id.rep_id)
        if report.rep_status == 'O' and report.rep_usr_id == request.user:
            break

    incidentSteps = IncidentStep.objects.filter(ins_inc_id=inc_id)
    entities = []
    for incidentStep in incidentSteps:
        entity = None
        if incidentStep.ins_type=='A':

            try:
                alert = Alert.objects.get(alt_id=incidentStep.ins_ent_id)

                entity = Entity(alert.alt_name, alert.alt_date, incidentStep.ins_type, "alerts:details", incidentStep.ins_id, alert.alt_id)

            except Maintenance.DoesNotExist:
                pass

        elif incidentStep.ins_type=='C':

            try:
                contact = Contact.objects.get(con_id=incidentStep.ins_ent_id)

                contact_name = ""
                if contact.con_direction=='I':
                    contact_name = request.user.__str__() + " > " + contact.con_address.__str__()
                else:
                    contact_name = contact.con_address.__str__() + " > " + request.user.__str__()

                entity = Entity(contact_name, contact.con_date, incidentStep.ins_type, "contacts:details", incidentStep.ins_id, contact.con_id)

            except Contact.DoesNotExist:
                pass

        elif incidentStep.ins_type=='M':

            try:
                maintenance = Maintenance.objects.get(mnt_id=incidentStep.ins_ent_id)

                entity = Entity(maintenance.mnt_name, maintenance.mnt_date, incidentStep.ins_type, "maintenances:details", incidentStep.ins_id, maintenance.mnt_id)

            except Maintenance.DoesNotExist:
                pass

        if entity != None:
            entities.append(entity)

    entities.sort(key=lambda x: x.ent_date, reverse=False)

    entity_id = 1
    for e in entities:
        e.ent_number = entity_id
        entity_id += 1

    alerts = Alert.objects.filter(alt_rep_id=report.rep_id)
    contacts = Contact.objects.filter(con_rep_id=report.rep_id)
    maintenances = Maintenance.objects.filter(mnt_rep_id=report.rep_id)

    incidentSteps = IncidentStep.objects.filter(ins_inc_id = inc_id)

    for iss in incidentSteps:
        if iss.ins_type == 'A':
            alerts = alerts.exclude( alt_id=iss.ins_ent_id )
        if iss.ins_type == 'C':
            contacts = contacts.exclude( con_id=iss.ins_ent_id )
        if iss.ins_type == 'M':
            maintenances = maintenances.exclude( mnt_id=iss.ins_ent_id )

    return render(request, 'main/reports/incidents/details.html', {'incident': Incident.objects.get(inc_id=inc_id), 'entities': entities, "report": report, "alerts": alerts, "contacts": contacts, "maintenances": maintenances})

def edit(request, rep_id, inc_id):
    report = Report.objects.get(rep_id=rep_id)
    incident = Incident.objects.get(inc_id=inc_id)
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            __modify(form, inc_id)
            return redirect("incidents:details", rep_id, inc_id)
        else:
            clear_custom_select_data(form.fields['inc_prj_id'])
            add_custom_select_data(form.fields['inc_prj_id'], int(form.cleaned_data['inc_prj_id'])-1, "selected")

    else:

            form = IncidentForm({   'inc_prj_id': incident.inc_prj_id.prj_id,
                                    'inc_ticket': incident.inc_ticket,
                                    'inc_date_start': str( incident.inc_date_start ),
                                    'inc_date_end': str( incident.inc_date_end ),
                                    'inc_com_id': incident.inc_com_id.com_value,
            })

            clear_custom_select_data(form.fields['inc_prj_id'])
            add_custom_select_data(form.fields['inc_prj_id'], int(incident.inc_prj_id.prj_id)-1, "selected")

    return render(request, 'main/reports/incidents/edit.html', {'incidentForm': form, 'incident': incident, 'report':report})

def __modify(form, inc_id):
    if form.is_valid():

        incident = Incident.objects.get(inc_id=inc_id)
        comment = Comment.objects.get(com_id=incident.inc_com_id.com_id)

        if form.cleaned_data.has_key('inc_prj_id'):
            incident.inc_prj_id = get_object_or_404(Project, prj_id=form.cleaned_data['inc_prj_id'])
        if form.cleaned_data.has_key('inc_ticket'):
            incident.inc_ticket = form.cleaned_data['inc_ticket']
        if form.cleaned_data.has_key('inc_date_start'):
            incident.inc_date_start = form.cleaned_data['inc_date_start']
        if form.cleaned_data.has_key('inc_date_end'):
            incident.inc_date_end = form.cleaned_data['inc_date_end']
        if form.cleaned_data.has_key('inc_com_id'):
            comment.com_value = form.cleaned_data['inc_com_id']

        comment.save()
        incident.save()

def close(request, inc_id, rep_id):
    if check_csrf(request):

        incident = Incident.objects.get(inc_id=inc_id)
        incident.inc_date_end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        incident.inc_status = 'R'
        incident.save()

    return redirect("reports:incident_tab", rep_id)

def invalidate(request, inc_id, rep_id):
    if check_csrf(request):

        incident = Incident.objects.get(inc_id=inc_id)
        incident.inc_date_end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        incident.inc_status = 'I'
        incident.save()

    return redirect("reports:incident_tab", rep_id)

def reopen(request, inc_id, rep_id):
    if check_csrf(request):

        incident = Incident.objects.get(inc_id=inc_id)
        incident.inc_date_end = None
        incident.inc_status = 'O'
        incident.save()

    return redirect("reports:incident_tab", rep_id)

def join_alert(request, rep_id, inc_id):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            alert = None
            if form.data.has_key('alt_id'):
                alert = get_object_or_404(Alert, alt_id=form.data['alt_id'])

            incident = Incident.objects.get(inc_id=inc_id)
            incidentStep = IncidentStep()
            incidentStep.ins_type = 'A'
            incidentStep.ins_ent_id = alert.alt_id
            incidentStep.ins_inc_id = incident
            incidentStepComment = Comment()
            incidentStepComment.save()
            incidentStep.ins_com_id = incidentStepComment
            incidentStep.save()
    return redirect("incidents:details", rep_id, inc_id)

def join_contact(request, rep_id, inc_id):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            contact = None
            if form.data.has_key('con_id'):
                contact = get_object_or_404(Contact, con_id=form.data['con_id'])
            incident = Incident.objects.get(inc_id=inc_id)
            incidentStep = IncidentStep()
            incidentStep.ins_type = 'C'
            incidentStep.ins_ent_id = contact.con_id
            incidentStep.ins_inc_id = incident
            incidentStepComment = Comment()
            incidentStepComment.save()
            incidentStep.ins_com_id = incidentStepComment
            incidentStep.save()
    return redirect("incidents:details", rep_id, inc_id)

def join_maintenance(request, rep_id, inc_id):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            maintenance = None
            if form.data.has_key('mnt_id'):
                maintenance = get_object_or_404(Maintenance, mnt_id=form.data['mnt_id'])
            incident = Incident.objects.get(inc_id=inc_id)
            incidentStep = IncidentStep()
            incidentStep.ins_type = 'M'
            incidentStep.ins_ent_id = maintenance.mnt_id
            incidentStep.ins_inc_id = incident
            incidentStepComment = Comment()
            incidentStepComment.save()
            incidentStep.ins_com_id = incidentStepComment
            incidentStep.save()
    return redirect("incidents:details", rep_id, inc_id)

def remove_incident_step(request, rep_id, ins_id):
    incidentStep = IncidentStep.objects.get(ins_id=ins_id)
    incidentStep.delete()
    return redirect("incidents:details", rep_id, incidentStep.ins_inc_id)
