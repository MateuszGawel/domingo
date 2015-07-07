from datetime import timedelta
from main.views.reports.utils import *
from django.shortcuts import redirect, render

def search(request):
    if request.method == 'GET':
        form = MaintenanceFilterForm(request.GET)
        print request.GET
        if doValidate(form):

            filter_result = Maintenance.objects.all()

            if form.cleaned_data.has_key('mnt_prj_id') and form.cleaned_data['mnt_prj_id'] != "":
                filter_result = filter_result.filter(mnt_prj_id=form.cleaned_data['mnt_prj_id'])

            if form.cleaned_data.has_key('mnt_usr_id') and form.cleaned_data['mnt_usr_id'] != "":
                user=User.objects.filter(username__contains=form.cleaned_data['mnt_usr_id'])
                reports = Report.objects.filter(rep_usr_id=user)
                filter_result = filter_result.filter(mnt_rep_id=reports)

            if form.cleaned_data.has_key('mnt_name') and form.cleaned_data['mnt_name'] != "":
                filter_result = filter_result.filter(mnt_name__contains=form.cleaned_data['mnt_name'])

            if form.cleaned_data.has_key('mnt_date_from') and form.cleaned_data['mnt_date_from'] is not None:
                filter_result = filter_result.filter(mnt_date__gte=form.cleaned_data['mnt_date_from'])

            if form.cleaned_data.has_key('mnt_date_to') and form.cleaned_data['mnt_date_to'] is not None:
                filter_result = filter_result.filter(mnt_date__lte=(form.cleaned_data['mnt_date_to']+timedelta(days=1)))

            return render(request, 'main/reports/maintenance_search.html', {'form': form, 'filter_result': filter_result})
        else:
            return render(request, 'main/reports/maintenance_search.html', {'form': form})
    else:
        form = MaintenanceFilterForm()
        return render(request, 'main/reports/maintenance_search.html', {'form': form})

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
