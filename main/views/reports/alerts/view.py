from django.shortcuts import redirect, render

from main.views.reports.utils import *


def details(request, rep_id, alt_id):
    report = Report.objects.get(rep_id=rep_id)
    alert = Alert.objects.get(alt_id=alt_id)
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if doValidate(form, request, alert.alt_rep_id):
            form.modify(alt_id)
            return redirect("alerts:details", rep_id, alt_id)
    else:
        form = AlertForm({'alert_project': alert.alt_prj_id.prj_id,
                           'alert_name': alert.alt_name,
                           'alert_ticket': alert.alt_ticket,
                           'alert_date': str( alert.alt_date ),
                           'alert_type': alert.alt_type,
                           'alert_comment': alert.alt_com_id.com_value})
    return render(request, 'main/reports/alerts/details.html', {'alert': alert, 'alertForm': form, 'report': report})

def remove(request, rep_id, alt_id):
    incidentSteps = IncidentStep.objects.filter(ins_ent_id=alt_id, ins_type='A')
    alert = Alert.objects.get(alt_id=alt_id)

    if request.method == 'POST':
        form = forms.Form(request.POST)
        if doValidate(form=form,request=request, report=alert.alt_rep_id):
            for step in incidentSteps:
                step.delete()
            alert.delete()
    return redirect("reports:alert_tab", alert.alt_rep_id)


def quick_edit(request, rep_id, alt_id):
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
        filledForm = AlertForm(request.POST)
        if doValidate(filledForm, request, alert.alt_rep_id):
            filledForm.modify(alt_id)
            return redirect("reports:alert_tab", rep_id)
        else:
            for i in range(0, len(filledAlertForms)):
                if int(filledAlertForms[i][0].alt_id) == int(request.POST['alt_id']):
                    filledAlertForms[i] = (Alert.objects.get(alt_id=request.POST['alt_id']), filledForm)
                    break

        return render(request, 'main/reports/alert_tab.html', {'alertForm': AlertForm(), 'alerts': filledAlertForms, 'report': report, 'inc_id': None, 'editingAlert': request.POST['alt_id']})
    else:
        return redirect("reports:alert_tab", rep_id)