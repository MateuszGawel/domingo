from django.shortcuts import redirect, render

from main.views.reports.utils import *


def details(request, rep_id, mnt_id):
    report = Report.objects.get(rep_id=rep_id)

    maintenance = Maintenance.objects.get(mnt_id=mnt_id)
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if doValidate(form, request, maintenance.mnt_rep_id):
            form.modify(mnt_id)
            return redirect("maintenances:details", rep_id, mnt_id)

    else:

        form = MaintenanceForm({'mnt_prj_id': maintenance.mnt_prj_id.prj_id,
                                'mnt_name': maintenance.mnt_name,
                                'mnt_date': str( maintenance.mnt_date ),
                                'mnt_com_id': maintenance.mnt_com_id.com_value,
        })

    return render(request, 'main/reports/maintenances/details.html', {'maintenanceForm': form, 'maintenance': maintenance, 'report': report})

def remove(request, rep_id, mnt_id):
    incidentSteps = IncidentStep.objects.filter(ins_ent_id=mnt_id, ins_type='M')
    maintenance = Maintenance.objects.get(mnt_id=mnt_id)
    if request.method == 'POST':
        form = forms.Form(request.POST)
        if doValidate(form=form,request=request, report=maintenance.mnt_rep_id):
            for step in incidentSteps:
                step.delete()
            maintenance.delete()

    return redirect("reports:maintenance_tab", maintenance.mnt_rep_id)

def quick_edit(request, rep_id, mnt_id):
    report = Report.objects.get(rep_id=rep_id)
    maintenance = Maintenance.objects.get(mnt_id=mnt_id)
    filledForm = None
    maintenances  = Maintenance.objects.filter(mnt_rep_id=report.rep_id)
    filledMaintenanceForms = []
    form = MaintenanceForm()

    for maintenance in maintenances:
        filledMaintenanceform = MaintenanceForm({'mnt_prj_id': maintenance.mnt_prj_id.prj_id,
                               'mnt_name': maintenance.mnt_name,
                               'mnt_date': str( maintenance.mnt_date ),
                               'mnt_com_id': maintenance.mnt_com_id.com_value})
        filledMaintenanceForms.append( (maintenance, filledMaintenanceform) )

    if request.method == 'POST':
        filledForm = MaintenanceForm(request.POST)
        if doValidate(filledForm, request, maintenance.mnt_rep_id):
            filledForm.modify(mnt_id)
            return redirect("reports:maintenance_tab", rep_id)
        else:
            for i in range(0, len(filledMaintenanceForms)):
                if int(filledMaintenanceForms[i][0].mnt_id) == int(request.POST['mnt_id']):
                    filledMaintenanceForms[i] = (Maintenance.objects.get(mnt_id=request.POST['mnt_id']), filledForm)
                    break

        return render(request, 'main/reports/maintenance_tab.html', {'maintenanceForm': form, 'maintenances': filledMaintenanceForms, 'report': report, 'inc_id': None, 'editingMaintenance': request.POST['mnt_id']})
    else:
        return redirect("reports:maintenance_tab", rep_id)
