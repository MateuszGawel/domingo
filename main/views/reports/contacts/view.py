from main.views.reports.utils import *
from django.shortcuts import redirect, render

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
                               'con_internal': contact.con_internal,
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
                               'con_internal': contact.con_internal,
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