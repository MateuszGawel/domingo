from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from main.views.reports.utils import *


def add(request):
    report = get_current_report(request)
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():

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

            return redirect("reports:edit")

        else:
            clear_custom_select_data(form.fields['alert_project'])
            add_custom_select_data(form.fields['alert_project'], int(form.cleaned_data['alert_project'])-1, "selected")
            clear_custom_select_data(form.fields['alert_type'])
            add_custom_select_data(form.fields['alert_type'], get_inner_tuple_index(Alert._meta.get_field('alt_type').choices, form.cleaned_data['alert_type'] ), "selected")

            messages.error(request, form.as_p())
            return redirect("reports:edit")
    else:
        return redirect("reports:edit")

def edit(request, alt_id):
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            alert_project = ""
            alert_name = ""
            alert_ticket = ""
            alert_date = ""
            alert_type = ""
            alert_comment = ""
            print form.cleaned_data['alert_project']

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

            alert = Alert.objects.get(alt_id=alt_id)
            alert.alt_prj_id = get_object_or_404(Project, prj_id=alert_project)
            alert.alt_name = alert_name
            alert.alt_ticket = alert_ticket
            alert.alt_date = alert_date
            alert.alt_type = alert_type
            comment = Comment.objects.get(com_id=alert.alt_com_id.com_id)
            comment.com_value = alert_comment
            comment.save()
            alert.alt_com_id = comment
            alert.save()

        else:
            clear_custom_select_data(form.fields['alert_project'])
            add_custom_select_data(form.fields['alert_project'], int(form.cleaned_data['alert_project'])-1, "selected")
            clear_custom_select_data(form.fields['alert_type'])
            add_custom_select_data(form.fields['alert_type'], get_inner_tuple_index(Alert._meta.get_field('alt_type').choices, form.cleaned_data['alert_type'] ), "selected")
            return render(request, 'main/reports/alerts/index.html', {'alertForm': form, 'alert': Alert.objects.get(alt_id=alt_id), 'editable': False})

    alert  = Alert.objects.get(alt_id=alt_id)
    print "##" ,alert.alt_date
    alertForm = AlertForm({'alert_project': alert.alt_prj_id.prj_id,
                           'alert_name': alert.alt_name,
                           'alert_ticket': alert.alt_ticket,
                           'alert_date': str( alert.alt_date ),
                           'alert_type': alert.alt_type,
                           'alert_comment': alert.alt_com_id.com_value})

    clear_custom_select_data(alertForm.fields['alert_project'])
    add_custom_select_data(alertForm.fields['alert_project'], alert.alt_prj_id.prj_id - 1, "selected")
    clear_custom_select_data(alertForm.fields['alert_type'])
    add_custom_select_data(alertForm.fields['alert_type'], get_inner_tuple_index(Alert._meta.get_field('alt_type').choices, alert.alt_type ), "selected")

    return render(request, 'main/reports/alerts/index.html', {'alertForm': alertForm, 'alert': alert, 'editable': True})

