from main.views.reports.utils import *
from django.shortcuts import redirect, render

def search(request):
    if request.method == 'GET':
        form = ContactFilterForm(request.GET)
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
        print form
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