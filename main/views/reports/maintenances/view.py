from django.shortcuts import get_object_or_404, redirect

from main.views.reports.utils import *


def details(request, rep_id, mnt_id):
    report = Report.objects.get(rep_id=rep_id)
    return render(request, 'main/reports/maintenances/details.html', {'maintenance': Maintenance.objects.get(mnt_id=mnt_id), 'report':report})

def remove(request, rep_id, mnt_id):
    incidentSteps = IncidentStep.objects.filter(ins_ent_id=mnt_id, ins_type='M')
    report = Report.objects.get(rep_id=rep_id)
    for step in incidentSteps:
        step.delete()

    maintenance = Maintenance.objects.get(mnt_id=mnt_id)
    maintenance.delete()

    return redirect("reports:maintenance_tab", maintenance.mnt_rep_id)

def edit(request, rep_id, mnt_id):
    report = Report.objects.get(rep_id=rep_id)

    maintenance = Maintenance.objects.get(mnt_id=mnt_id)
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            __modify(form, mnt_id)
            return redirect("maintenances:details", rep_id, mnt_id)
        else:
            clear_custom_select_data(form.fields['mnt_prj_id'])
            add_custom_select_data(form.fields['mnt_prj_id'], int(form.cleaned_data['mnt_prj_id'])-1, "selected")

    else:

        form = MaintenanceForm({'mnt_prj_id': maintenance.mnt_prj_id.prj_id,
                                'mnt_name': maintenance.mnt_name,
                                'mnt_date': str( maintenance.mnt_date ),
                                'mnt_com_id': maintenance.mnt_com_id.com_value,
        })

        clear_custom_select_data(form.fields['mnt_prj_id'])

    return render(request, 'main/reports/maintenances/edit.html', {'maintenanceForm': form, 'maintenance': maintenance, 'report': report})

def __modify(form, mnt_id):
    if form.is_valid():

        maintenance = Maintenance.objects.get(mnt_id=mnt_id)
        comment = Comment.objects.get(com_id=maintenance.mnt_com_id.com_id)

        if form.cleaned_data.has_key('mnt_prj_id'):
            maintenance.mnt_prj_id = get_object_or_404(Project, prj_id=form.cleaned_data['mnt_prj_id'])
        if form.cleaned_data.has_key('mnt_name'):
            maintenance.mnt_name = form.cleaned_data['mnt_name']
        if form.cleaned_data.has_key('mnt_date'):
            maintenance.mnt_date = form.cleaned_data['mnt_date']
        if form.cleaned_data.has_key('mnt_com_id'):
            comment.com_value = form.cleaned_data['mnt_com_id']

        comment.save()
        maintenance.save()