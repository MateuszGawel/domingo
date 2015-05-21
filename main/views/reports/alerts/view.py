from django.shortcuts import get_object_or_404, redirect

from main.views.reports.utils import *


def details(request, rep_id, alt_id):
    report = Report.objects.get(rep_id=rep_id)
    return render(request, 'main/reports/alerts/details.html', {'alert': Alert.objects.get(alt_id=alt_id), 'report':report})

def remove(request, rep_id, alt_id):
    incidentSteps = IncidentStep.objects.filter(ins_ent_id=alt_id, ins_type='A')
    for step in incidentSteps:
        step.delete()

    alert = Alert.objects.get(alt_id=alt_id)
    alert.delete()
    return redirect("reports:alert_tab", alert.alt_rep_id)

def edit(request, rep_id, alt_id):
    report = Report.objects.get(rep_id=rep_id)
    alert = Alert.objects.get(alt_id=alt_id)
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            __modify(form, alt_id)
            return redirect("alerts:details", rep_id, alt_id)
        else:
            clear_custom_select_data(form.fields['alert_project'])
            add_custom_select_data(form.fields['alert_project'], int(form.cleaned_data['alert_project'])-1, "selected")
            clear_custom_select_data(form.fields['alert_type'])
            add_custom_select_data(form.fields['alert_type'], get_inner_tuple_index(Alert._meta.get_field('alt_type').choices, form.cleaned_data['alert_type'] ), "selected")

    else:
        form = AlertForm({'alert_project': alert.alt_prj_id.prj_id,
                               'alert_name': alert.alt_name,
                               'alert_ticket': alert.alt_ticket,
                               'alert_date': str( alert.alt_date ),
                               'alert_type': alert.alt_type,
                               'alert_comment': alert.alt_com_id.com_value})

        clear_custom_select_data(form.fields['alert_project'])
        add_custom_select_data(form.fields['alert_project'], alert.alt_prj_id.prj_id - 1, "selected")
        clear_custom_select_data(form.fields['alert_type'])
        add_custom_select_data(form.fields['alert_type'], get_inner_tuple_index(Alert._meta.get_field('alt_type').choices, alert.alt_type ), "selected")

    return render(request, 'main/reports/alerts/edit.html', {'alertForm': form, 'alert': alert, 'report': report})

def quick_edit(request, rep_id, alt_id):
    report = Report.objects.get(rep_id=rep_id)
    alert = Alert.objects.get(alt_id=alt_id)
    filledForm = None
    alerts  = Alert.objects.filter(alt_rep_id=report.rep_id)
    filledAlertForms = []
    form = AlertForm()
    clear_custom_select_data(form.fields['alert_project'])
    clear_custom_select_data(form.fields['alert_type'])

    for alert in alerts:
        filledAlertform = AlertForm({'alert_project': alert.alt_prj_id.prj_id,
                               'alert_name': alert.alt_name,
                               'alert_ticket': alert.alt_ticket,
                               'alert_date': str( alert.alt_date ),
                               'alert_type': alert.alt_type,
                               'alert_comment': alert.alt_com_id.com_value})
        clear_custom_select_data(filledAlertform.fields['alert_project'])
        add_custom_select_data(filledAlertform.fields['alert_project'], alert.alt_prj_id.prj_id - 1, "selected")
        clear_custom_select_data(filledAlertform.fields['alert_type'])
        add_custom_select_data(filledAlertform.fields['alert_type'], get_inner_tuple_index(Alert._meta.get_field('alt_type').choices, alert.alt_type ), "selected")
        filledAlertForms.append( (alert, filledAlertform) )

    if request.method == 'POST':
        filledForm = AlertForm(request.POST)
        if filledForm.is_valid():
            __modify(filledForm, alt_id)
            return redirect("reports:alert_tab", rep_id)
        else:
            for i in range(0, len(filledAlertForms)):
                if int(filledAlertForms[i][0].alt_id) == int(request.POST['alt_id']):
                    filledAlertForms[i] = (Alert.objects.get(alt_id=request.POST['alt_id']), filledForm)
                    break

            clear_custom_select_data(filledForm.fields['alert_project'])
            add_custom_select_data(filledForm.fields['alert_project'], int(filledForm.cleaned_data['alert_project'])-1, "selected")
            clear_custom_select_data(filledForm.fields['alert_type'])
            add_custom_select_data(filledForm.fields['alert_type'], get_inner_tuple_index(Alert._meta.get_field('alt_type').choices, filledForm.cleaned_data['alert_type'] ), "selected")

    return render(request, 'main/reports/alert_tab.html', {'alertForm': form, 'alerts': filledAlertForms, 'report': report, 'inc_id': None, 'editingAlert': request.POST['alt_id']})

def __modify(form, alt_id):
    if form.is_valid():

        alert = Alert.objects.get(alt_id=alt_id)
        comment = Comment.objects.get(com_id=alert.alt_com_id.com_id)

        if form.cleaned_data.has_key('alert_project'):
            alert.alt_prj_id = get_object_or_404(Project, prj_id = form.cleaned_data['alert_project'] )
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
        alert.save()