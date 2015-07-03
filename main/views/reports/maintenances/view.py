from main.views.reports.utils import *
from django.shortcuts import redirect, render

def search(request):
    if request.method == 'GET':
        form = MaintenanceFilterForm(request.GET)
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
