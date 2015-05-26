from main.views.reports.utils import *


def details(request, rep_id, con_id):
    report = Report.objects.get(rep_id=rep_id)
    return render(request, 'main/reports/contacts/details.html', {'contact': Contact.objects.get(con_id=con_id), 'report':report})

def remove(request, rep_id, con_id):
    report = Report.objects.get(rep_id=rep_id)
    incidentSteps = IncidentStep.objects.filter(ins_ent_id=con_id, ins_type='C')
    for step in incidentSteps:
        step.delete()

    contact = Contact.objects.get(con_id=con_id)
    contact.delete()
    return redirect("reports:contact_tab", contact.con_rep_id)

def edit(request, rep_id, con_id):
    report = Report.objects.get(rep_id=rep_id)
    contact = Contact.objects.get(con_id=con_id)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            __modify(form, con_id)
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

    return render(request, 'main/reports/contacts/edit.html', {'contactForm': form, 'contact': contact, 'report':report})

def __modify(form, con_id):
    if form.is_valid():

        contact = Contact.objects.get(con_id=con_id)
        comment = Comment.objects.get(com_id=contact.con_com_id.com_id)

        if form.cleaned_data.has_key('con_prj_id'):
            contact.con_prj_id = get_object_or_404(Project, prj_id=form.cleaned_data['con_prj_id'])
        if form.cleaned_data.has_key('con_type'):
            contact.con_type = form.cleaned_data['con_type']
        if form.cleaned_data.has_key('con_address'):
            contact.con_address = form.cleaned_data['con_address']
        if form.cleaned_data.has_key('con_date'):
            contact.con_date = form.cleaned_data['con_date']
        if form.cleaned_data.has_key('con_direction'):
            contact.con_direction = form.cleaned_data['con_direction']
        if form.cleaned_data.has_key('con_internal'):
            contact.con_internal = form.cleaned_data['con_internal']
        if form.cleaned_data.has_key('con_com_id'):
            comment.com_value = form.cleaned_data['con_com_id']

        comment.save()
        contact.save()