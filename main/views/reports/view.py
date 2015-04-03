import datetime
from django.shortcuts import redirect
from django.contrib.messages import get_messages
from utils import *

def index(request):
    if request.user.is_authenticated():
        report = Report.objects.filter(rep_usr_id=request.user.id)
        if report.exists():
            report = report.latest('rep_id')
        else:
            report = None
        return render(request, 'main/reports/index.html', {'report': report, 'user': request.user})
    else:
        return render(request, 'main/login.html', None)

def search(request):
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


            return render(request, 'main/reports/search.html', {'form': form, 'filter_result': filter_result})
        else:
            return render(request, 'main/reports/search.html', {'form': form})
    else:
        return search(request) #?

def create(request):
    if check_csrf(request):

        if Report.objects.filter(rep_usr_id=request.user.id, rep_date_sent=None).exists():
            return redirect("reports:index")
        report = Report()
        report.rep_status = 'O'
        report.rep_date_created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report.rep_usr_id = request.user
        report.rep_notes = 'Siema, elo, mowi Spejson'
        report.save()
        return redirect("reports:edit")

    return redirect("reports:index")

def edit(request):
    if request.user.is_authenticated():
        report = get_current_report(request)

        alertForm = AlertForm()
        clear_custom_select_data(alertForm.fields['alert_project'])
        clear_custom_select_data(alertForm.fields['alert_type'])

        alertForm = alertForm.as_p()

        alerts  = Alert.objects.filter(alt_rep_id=report.rep_id)

        storage = get_messages(request)
        count = 0;
        for message in storage:
            alertForm = message

        contactForm = ContactForm()

        contacts = Contact.objects.filter(con_rep_id=report.rep_id)

        return render(request, 'main/reports/browse.html', {'alertForm': alertForm, 'contactForm': contactForm, 'alerts': alerts, 'contacts': contacts})

    else:
        return render(request, 'main/login.html', {'error_message': "You have to log in first."})

def close(request):
    if check_csrf(request):

        report = get_current_report(request)
        report.rep_date_sent = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report.rep_status = 'S'
        report.save()

    return redirect("reports:index")
