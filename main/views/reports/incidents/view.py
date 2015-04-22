from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from main.views.reports.utils import *
import datetime


class Entity:

    def __init__(self, name, date, type, url, id):
        self.ent_name = name
        self.ent_date = date
        self.ent_type = type

        self.ent_url = url

        self.ent_id = id


def details(request, inc_id):

    incidentSteps = IncidentStep.objects.filter(ins_inc_id=inc_id)
    entities = []
    for incidentStep in incidentSteps:
        entity = None
        if incidentStep.ins_type=='A':
            alert = Alert.objects.get(alt_id=incidentStep.ins_ent_id)
            entity = Entity(alert.alt_name, alert.alt_date, incidentStep.ins_type, "alerts:details", alert.alt_id)
        elif incidentStep.ins_type=='C':
            contact = Contact.objects.get(con_id=incidentStep.ins_ent_id)
            contact_name = ""
            if contact.con_direction=='I':
                contact_name = request.user.__str__() + " > " + contact.con_address.__str__()
            else:
                contact_name = contact.con_address.__str__() + " > " + request.user.__str__()
            entity = Entity(contact_name, contact.con_date, incidentStep.ins_type, "contacts:details", contact.con_id)
        entities.append(entity)
    return render(request, 'main/reports/incidents/details.html', {'incident': Incident.objects.get(inc_id=inc_id), 'entities': entities})

def edit(request, inc_id):
    incident = Incident.objects.get(inc_id=inc_id)
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            __modify(form, inc_id)
            return redirect("incidents:details", inc_id)
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

    return render(request, 'main/reports/incidents/edit.html', {'incidentForm': form, 'incident': incident})

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