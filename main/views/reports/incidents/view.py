from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from main.views.reports.utils import *



def details(request, con_id):
    return render(request, 'main/reports/contacts/details.html', {'contact': Contact.objects.get(con_id=con_id)})

def edit(request, con_id):
    contact = Contact.objects.get(con_id=con_id)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            __modify(form, con_id)
            return redirect("contacts:details", con_id)
        else:
            clear_custom_select_data(form.fields['con_prj_id'])
            add_custom_select_data(form.fields['con_prj_id'], int(form.cleaned_data['con_prj_id'])-1, "selected")
            clear_custom_select_data(form.fields['con_type'])
            add_custom_select_data(form.fields['con_type'], get_inner_tuple_index(Contact._meta.get_field('con_type').choices, form.cleaned_data['con_type'] ), "selected")
            clear_custom_select_data(form.fields['con_direction'])
            add_custom_select_data(form.fields['con_direction'], get_inner_tuple_index(Contact._meta.get_field('con_direction').choices, form.cleaned_data['con_direction'] ), "selected")

    else:

        form = ContactForm({   'con_prj_id': contact.con_prj_id.prj_id,
                               'con_type': contact.con_type,
                               'con_address': contact.con_address,
                               'con_date': str( contact.con_date ),
                               'con_direction': contact.con_direction,
                               'con_internal': contact.con_internal,
                               'con_com_id': contact.con_com_id.com_value,
        })

        clear_custom_select_data(form.fields['con_prj_id'])
        add_custom_select_data(form.fields['con_prj_id'], contact.con_prj_id.prj_id - 1, "selected")
        clear_custom_select_data(form.fields['con_type'])
        add_custom_select_data(form.fields['con_type'], get_inner_tuple_index(Contact._meta.get_field('con_type').choices, contact.con_type ), "selected")
        clear_custom_select_data(form.fields['con_direction'])
        add_custom_select_data(form.fields['con_direction'], get_inner_tuple_index(Contact._meta.get_field('con_direction').choices, contact.con_direction ), "selected")

    return render(request, 'main/reports/contacts/edit.html', {'contactForm': form, 'contact': contact})

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