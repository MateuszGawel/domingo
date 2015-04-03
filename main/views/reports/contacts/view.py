from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from main.views.reports.utils import *


def add(request):
    report = get_current_report(request)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            contact = Contact()
            comment = Comment()

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

                print "@@@@@@@@@@ ", form.cleaned_data['con_internal']

                print "@@@@@@@@@@ ", contact.con_internal
            if form.cleaned_data.has_key('con_com_id'):
                comment.com_value = form.cleaned_data['con_com_id']

            comment.save()

            contact.con_com_id = comment
            contact.con_rep_id = report

            contact.save()

            return redirect("reports:edit")

        else:
            # clear_custom_select_data(form.fields['alert_project'])
            # add_custom_select_data(form.fields['alert_project'], int(form.cleaned_data['alert_project'])-1, "selected")
            # clear_custom_select_data(form.fields['alert_type'])
            # add_custom_select_data(form.fields['alert_type'], get_inner_tuple_index(Alert._meta.get_field('alt_type').choices, form.cleaned_data['alert_type'] ), "selected")
            #
            # messages.error(request, form.as_p())
            return redirect("reports:edit")
    else:
        return redirect("reports:edit")

def edit(request, con_id):
    redirect("reports:edit")

