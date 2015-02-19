from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from main.models import Alert, Comment
import datetime
from django.db.models import Max
from main.forms import *
from django.contrib import messages
from django.contrib.messages import get_messages

def reports(request):
    if request.user.is_authenticated():
        report = Report.objects.filter(rep_usr_id=request.user.id)
        if report.exists():
            report = report.latest('rep_id')
        else:
            report = None
        return render(request, 'main/reports.html', {'report': report, 'user': request.user})
    else:
        return render(request, 'main/login.html', None)

def add_alert(request):
    report = __get_current_report(request)
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            alert_project = ""
            alert_name = ""
            alert_ticket = ""
            alert_date = ""
            alert_type = ""
            alert_comment = ""
            print form.cleaned_data['alert_project']

            if form.cleaned_data.has_key('alert_project'):
                alert_project = form.cleaned_data['alert_project']
            if form.cleaned_data.has_key('alert_name'):
                alert_name = form.cleaned_data['alert_name']
            if form.cleaned_data.has_key('alert_ticket'):
                alert_ticket = form.cleaned_data['alert_ticket']
            if form.cleaned_data.has_key('alert_date'):
                alert_date = form.cleaned_data['alert_date']
            if form.cleaned_data.has_key('alert_type'):
                alert_type = form.cleaned_data['alert_type']
            if form.cleaned_data.has_key('alert_comment'):
                alert_comment = form.cleaned_data['alert_comment']

            alert = Alert()
            alert.alt_prj_id = get_object_or_404(Project, prj_id=alert_project)
            alert.alt_name = alert_name
            alert.alt_ticket = alert_ticket
            alert.alt_date = alert_date
            alert.alt_type = alert_type
            comment = Comment()
            comment.com_value = alert_comment
            comment.save()
            alert.alt_com_id = comment
            alert.alt_rep_id = report

            alert.save()
            return redirect("main:edit_report")
        else:
            clear_custom_select_data(form.fields['alert_project'])
            add_custom_select_data(form.fields['alert_project'], int(form.cleaned_data['alert_project'])-1, "selected")
            clear_custom_select_data(form.fields['alert_type'])
            add_custom_select_data(form.fields['alert_type'], getInnerTupleIndex(Alert._meta.get_field('alt_type').choices, form.cleaned_data['alert_type'] ), "selected")
            alerts  = Alert.objects.filter(alt_rep_id=report.rep_id)

            messages.error(request, form)
            return redirect("main:edit_report")
            #return render(request, 'main/report_creation.html', {'form': form, 'alerts': alerts, 'error_message': "Alert has NOT been added"})
    else:
        return redirect("main:edit_report")

def add_contact(request):
    pass

def clear_custom_select_data(formField):
    '''Czyscimy tutaj custom data z fielda czyli caly kontekst 'value' jesli jest wyslany. czyli w tym wypadku selected dla taga <option>. Mozemy dodac tutaj wiecej.
    Jak tego nie robilismy to mimo odpowiedniego value i tak renderowana byla pierwsza opcja z listy.'''
    numberOfOptions = len( formField.widget.widget_context['values'] )

    for i in range( numberOfOptions ):
        currentOptionValues = formField.widget.widget_context['values'][i]
        formField.widget.widget_context['values'][i] =( currentOptionValues[0], currentOptionValues[1], "" )

def add_custom_select_data(formField, optionIndex, valueValue):
    values = formField.widget.widget_context['values'][optionIndex]
    formField.widget.widget_context['values'][optionIndex] =( values[0], values[1], valueValue )

def getInnerTupleIndex(baseTuple, element):
    '''Potrzebne zeby wziac index wewnetrznego tuple'a z choices modelu - nie bedzie potrzebne jesli zamiast tego choices typy alertow itp wrzucimy do tabel'''
    for i in range( len(baseTuple) ):
        if element in baseTuple[i]:
            return i
        else:
            print "nie znalazlem ", element, " w ", baseTuple[i], " | a index to ", i
    return -1

def create_report(request):
    if Report.objects.filter(rep_usr_id=request.user.id, rep_date_sent=None).exists():
        return redirect("main:reports")
    report = Report()
    report.rep_status = 'O'
    report.rep_date_created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report.rep_usr_id = request.user
    report.rep_notes = 'Siema, elo, mowi Spejson'
    report.save()
    return redirect("main:edit_report")

def edit_report(request):
    if request.user.is_authenticated():
        report = __get_current_report(request);

        alertForm = AlertForm()
        clear_custom_select_data(alertForm.fields['alert_project'])
        clear_custom_select_data(alertForm.fields['alert_type'])
        alerts  = Alert.objects.filter(alt_rep_id=report.rep_id)



        storage = get_messages(request)
        count = 0;
        for message in storage:
            alertForm = AlertForm(message)

        contactForm = ContactForm()
        return render(request, 'main/report_creation.html', {'alertForm': alertForm, 'contactForm': contactForm, 'alerts': alerts})
    else:
        return render(request, 'main/login.html', {'error_message': "You have to log in first."})

def close_report(request):
    report = __get_current_report(request)
    report.rep_date_sent = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report.rep_status = 'S'
    report.save()
    return redirect("main:reports")

def __get_current_report(request):
    report = Report.objects.filter(rep_usr_id=request.user.id, rep_date_sent=None).latest('rep_id')
    return report

def browse_reports(request):
    if request.user.is_authenticated():
        f = ReportFilterForm()
        return render(request, 'main/report_browse.html', {'form': f, 'filter_result': None})
    else:
        return render(request, 'main/login.html', {'error_message': "You have to log in first."})

def browse_my_reports(request):
    print "user: " + str(request.user.id)
    if request.user.is_authenticated():
        f = ReportFilterForm()
        f.rep_usr_id = request.user.id
        result = Report.objects.filter(rep_usr_id=request.user.id)
        print result
        return render(request, 'main/report_browse.html', {'form': f, 'filter_result': result})
    else:
        return render(request, 'main/login.html', {'error_message': "You have to log in first."})

def edit_alert(request, alt_id):
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            alert_project = ""
            alert_name = ""
            alert_ticket = ""
            alert_date = ""
            alert_type = ""
            alert_comment = ""
            print form.cleaned_data['alert_project']

            if form.cleaned_data.has_key('alert_project'):
                alert_project = form.cleaned_data['alert_project']
            if form.cleaned_data.has_key('alert_name'):
                alert_name = form.cleaned_data['alert_name']
            if form.cleaned_data.has_key('alert_ticket'):
                alert_ticket = form.cleaned_data['alert_ticket']
            if form.cleaned_data.has_key('alert_date'):
                alert_date = form.cleaned_data['alert_date']
            if form.cleaned_data.has_key('alert_type'):
                alert_type = form.cleaned_data['alert_type']
            if form.cleaned_data.has_key('alert_comment'):
                alert_comment = form.cleaned_data['alert_comment']

            alert = Alert.objects.get(alt_id=alt_id)
            alert.alt_prj_id = get_object_or_404(Project, prj_id=alert_project)
            alert.alt_name = alert_name
            alert.alt_ticket = alert_ticket
            alert.alt_date = alert_date
            alert.alt_type = alert_type
            comment = Comment.objects.get(com_id=alert.alt_com_id.com_id)
            comment.com_value = alert_comment
            comment.save()
            alert.alt_com_id = comment
            alert.save()
            return __alert_details(request, alt_id)
        else:
            clear_custom_select_data(form.fields['alert_project'])
            add_custom_select_data(form.fields['alert_project'], int(form.cleaned_data['alert_project'])-1, "selected")
            clear_custom_select_data(form.fields['alert_type'])
            add_custom_select_data(form.fields['alert_type'], getInnerTupleIndex(Alert._meta.get_field('alt_type').choices, form.cleaned_data['alert_type'] ), "selected")
            return render(request, 'main/alert_details.html', {'alertForm': form, 'alert': Alert.objects.get(alt_id=alt_id), 'editable': False})
    else:
        return __alert_details(request, alt_id)

def __alert_details(request, alt_id):
    alert  = Alert.objects.get(alt_id=alt_id)
    print "##" ,alert.alt_date
    alertForm = AlertForm({'alert_project': alert.alt_prj_id.prj_id,
                           'alert_name': alert.alt_name,
                           'alert_ticket': alert.alt_ticket,
                           'alert_date': str( alert.alt_date ),
                           'alert_type': alert.alt_type,
                           'alert_comment': alert.alt_com_id.com_value})

    clear_custom_select_data(alertForm.fields['alert_project'])
    add_custom_select_data(alertForm.fields['alert_project'], alert.alt_prj_id.prj_id - 1, "selected")
    clear_custom_select_data(alertForm.fields['alert_type'])
    add_custom_select_data(alertForm.fields['alert_type'], getInnerTupleIndex(Alert._meta.get_field('alt_type').choices, alert.alt_type ), "selected")

    return render(request, 'main/alert_details.html', {'alertForm': alertForm, 'alert': alert, 'editable': True})

def filter_reports(request):
    if request.method == 'GET':
        form = ReportFilterForm(request.GET)
        if form.is_valid():
            filter_result = Report.objects.all()

            if form.cleaned_data.has_key('rep_id') and form.cleaned_data['rep_id'] != "":
                filter_result = filter_result.filter(rep_id=form.cleaned_data['rep_id'])

            if form.cleaned_data.has_key('rep_status') and form.cleaned_data['rep_status'] != "":
                filter_result = filter_result.filter(rep_status=form.cleaned_data['rep_status'])

            if form.cleaned_data.has_key('rep_date_created_from') and form.cleaned_data['rep_date_created_from'] is not None:
                filter_result = filter_result.filter(rep_date_created__gte=form.cleaned_data['rep_date_created_from'])

            if form.cleaned_data.has_key('rep_date_created_to') and form.cleaned_data['rep_date_created_to'] is not None:
                filter_result = filter_result.filter(rep_date_created__lte=form.cleaned_data['rep_date_created_to'])

            if form.cleaned_data.has_key('rep_date_sent_from') and form.cleaned_data['rep_date_sent_from'] is not None:
                filter_result = filter_result.filter(rep_date_sent__gte=form.cleaned_data['rep_date_sent_from'])

            if form.cleaned_data.has_key('rep_date_sent_to') and form.cleaned_data['rep_date_sent_to'] is not None:
                filter_result = filter_result.filter(rep_date_sent__lte=form.cleaned_data['rep_date_sent_to'])

            if form.cleaned_data.has_key('rep_date_removed_from') and form.cleaned_data['rep_date_removed_from'] is not None:
                filter_result = filter_result.filter(rep_date_removed__gte=form.cleaned_data['rep_date_removed_from'])

            if form.cleaned_data.has_key('rep_date_removed_to') and form.cleaned_data['rep_date_removed_to'] is not None:
                filter_result = filter_result.filter(rep_date_removed__lte=form.cleaned_data['rep_date_removed_to'])

            if form.cleaned_data.has_key('rep_usr_id') and form.cleaned_data['rep_usr_id'] != "":
                filter_result = filter_result.filter(rep_usr_id=form.cleaned_data['rep_usr_id'])


            return render(request, 'main/report_browse.html', {'form': form, 'filter_result': filter_result})
        else:
            return render(request, 'main/report_browse.html', {'form': form})
    else:
        return browse_reports(request)
