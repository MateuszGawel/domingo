from datetime import timedelta
from main.views.reports.utils import *
from django.shortcuts import redirect, render

def search(request):
    if request.method == 'GET':
        form = ContactFilterForm(request.GET)
        if doValidate(form):

            filter_result = Contact.objects.all()

            if form.cleaned_data.has_key('con_prj_id') and form.cleaned_data['con_prj_id'] != "":
                filter_result = filter_result.filter(con_prj_id=form.cleaned_data['con_prj_id'])

            if form.cleaned_data.has_key('con_usr_id') and form.cleaned_data['con_usr_id'] != "":
                user=User.objects.filter(username__contains=form.cleaned_data['con_usr_id'])
                reports = Report.objects.filter(rep_usr_id=user)
                filter_result = filter_result.filter(con_rep_id=reports)

            if form.cleaned_data.has_key('con_address') and form.cleaned_data['con_address'] != "":
                filter_result = filter_result.filter(con_address__contains=form.cleaned_data['con_address'])

            if form.cleaned_data.has_key('con_scope') and form.cleaned_data['con_scope'] != "":
                filter_result = filter_result.filter(con_scope=form.cleaned_data['con_scope'])

            if form.cleaned_data.has_key('con_type') and form.cleaned_data['con_type'] != "":
                filter_result = filter_result.filter(con_type=form.cleaned_data['con_type'])

            if form.cleaned_data.has_key('con_direction') and form.cleaned_data['con_direction'] != "":
                filter_result = filter_result.filter(con_direction=form.cleaned_data['con_direction'])

            if form.cleaned_data.has_key('con_date_from') and form.cleaned_data['con_date_from'] is not None:
                filter_result = filter_result.filter(con_date__gte=form.cleaned_data['con_date_from'])

            if form.cleaned_data.has_key('con_date_to') and form.cleaned_data['con_date_to'] is not None:
                filter_result = filter_result.filter(con_date__lte=(form.cleaned_data['con_date_to']+timedelta(days=1)))

            return render(request, 'main/reports/contact_search.html', {'form': form, 'filter_result': filter_result})
        else:
            return render(request, 'main/reports/contact_search.html', {'form': form})
    else:
        form = ContactFilterForm()
        return render(request, 'main/reports/contact_search.html', {'form': form})

def details(request, rep_id, con_id):
    report = Report.objects.get(rep_id=rep_id)
    contact = Contact.objects.get(con_id=con_id)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if doValidate(form, request, contact.con_rep_id):
            form.modify(con_id)
            return redirect("contacts:details", rep_id, con_id)
    else:
        form = ContactForm({   'con_prj_id': contact.con_prj_id.prj_id,
                               'con_type': contact.con_type,
                               'con_address': contact.con_address,
                               'con_date': str( contact.con_date ),
                               'con_direction': contact.con_direction,
                               'con_scope': contact.con_scope,
                               'con_com_id': contact.con_com_id.com_value,
        })
    return render(request, 'main/reports/contacts/details.html', {'contactForm': form, 'contact': contact, 'report':report})


def remove(request, rep_id, con_id):
    incidentSteps = IncidentStep.objects.filter(ins_ent_id=con_id, ins_type='C')
    contact = Contact.objects.get(con_id=con_id)
    if request.method == 'POST':
        form = forms.Form(request.POST)
        if doValidate(form=form,request=request, report=contact.con_rep_id):
            for step in incidentSteps:
                step.delete()
            contact.delete()
    return redirect("reports:contact_tab", contact.con_rep_id)


def quick_edit(request, rep_id, con_id):
    report = Report.objects.get(rep_id=rep_id)
    contact = Contact.objects.get(con_id=con_id)
    filledForm = None
    contacts  = Contact.objects.filter(con_rep_id=report.rep_id)
    filledContactForms = []
    form = ContactForm()

    for contact in contacts:
        filledContactform = ContactForm({'con_prj_id': contact.con_prj_id.prj_id,
                               'con_type': contact.con_type,
                               'con_address': contact.con_address,
                               'con_date': str( contact.con_date ),
                               'con_direction': contact.con_direction,
                               'con_scope': contact.con_scope,
                               'con_com_id': contact.con_com_id.com_value})
        filledContactForms.append( (contact, filledContactform) )

    if request.method == 'POST':
        filledForm = ContactForm(request.POST)
        if doValidate(filledForm, request, contact.con_rep_id):
            filledForm.modify(con_id)
            return redirect("reports:contact_tab", rep_id)
        else:
            for i in range(0, len(filledContactForms)):
                if int(filledContactForms[i][0].con_id) == int(request.POST['con_id']):
                    filledContactForms[i] = (Contact.objects.get(con_id=request.POST['con_id']), filledForm)
                    break

        return render(request, 'main/reports/contact_tab.html', {'contactForm': form, 'contacts': filledContactForms, 'report': report, 'inc_id': None, 'editingContact': request.POST['con_id']})
    else:
        return redirect("reports:contact_tab", rep_id)