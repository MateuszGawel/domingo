from main.views.reports.utils import *
from django.shortcuts import redirect, render

def search(request):
    if request.method == 'GET':
        form = AlertFilterForm(request.GET)
        print request.GET
        if doValidate(form):

            filter_result = Report.objects.all()
            '''
            if form.cleaned_data.has_key('rep_id') and form.cleaned_data['rep_id'] != "":
                filter_result = filter_result.filter(rep_id=form.cleaned_data['rep_id'])

            if form.cleaned_data.has_key('rep_status') and form.cleaned_data['rep_status'] != "":
                filter_result = filter_result.filter(rep_status=form.cleaned_data['rep_status'])

            if form.cleaned_data.has_key('rep_date_created_from') and form.cleaned_data['rep_date_created_from'] is not None:
                filter_result = filter_result.filter(rep_date_created__gte=form.cleaned_data['rep_date_created_from'])

            if form.cleaned_data.has_key('rep_date_created_to') and form.cleaned_data['rep_date_created_to'] is not None:
                filter_result = filter_result.filter(rep_date_created__lte=(form.cleaned_data['rep_date_created_to']+timedelta(days=1)))

            if form.cleaned_data.has_key('rep_date_sent_from') and form.cleaned_data['rep_date_sent_from'] is not None:
                filter_result = filter_result.filter(rep_date_sent__gte=form.cleaned_data['rep_date_sent_from'])

            if form.cleaned_data.has_key('rep_date_sent_to') and form.cleaned_data['rep_date_sent_to'] is not None:
                filter_result = filter_result.filter(rep_date_sent__lte=(form.cleaned_data['rep_date_sent_to']+timedelta(days=1)))

            if form.cleaned_data.has_key('rep_usr_id') and form.cleaned_data['rep_usr_id'] != "":
                filter_result = filter_result.filter(rep_usr_id=User.objects.get(username=form.cleaned_data['rep_usr_id']))
            '''
            return render(request, 'main/reports/alert_search.html', {'form': form, 'filter_result': filter_result})
        else:
            return render(request, 'main/reports/alert_search.html', {'form': form})
    else:
        form = AlertFilterForm()
        return render(request, 'main/reports/alert_search.html', {'form': form})

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