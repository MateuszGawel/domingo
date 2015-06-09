from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

from main.models import *


class CustomWidget(forms.Widget):

    #tu nie moze byc konstruktora - nadpisalibysmy init Widgeta, w ktorym ustawia sobie rozne rzeczy a z jakiegos powodu nie moge wywolac super.__init__() poprawnie
    template_name = ""
    label = ""
    widget_context = {}

    def set_template_name(self, t):
        self.template_name = t

    def set_label(self, l):
        self.label = l

    def set_context(self, d):
        self.widget_context = d

    def render(self, name, value, attrs=None):
        if value is not None:
            context = {'label': self.label, 'name': name, 'value': value}
        else:
            context = {'label': self.label, 'name': name}
        context = dict(context.items() + self.widget_context.items())

        return mark_safe(render_to_string(self.template_name, context))

class MyWidget:
    widgetID = ""

    def get_widget(self):
        return self.widget


class DateWidget(MyWidget):

    def __init__(self, label):
        self.widget = CustomWidget()

        self.widget.set_template_name('main/_widgets/date_widget.html')
        self.widget.set_label(label)

        context = {'placeholder': 'YYYY-MM-DD hh:mm:ss', 'error': False}

        self.widget.set_context(context)

class MinDateWidget(MyWidget):

    def __init__(self, label):
        self.widget = CustomWidget()
        self.widget.set_template_name('main/_widgets/min_date_widget.html')
        context = {'placeholder': 'YYYY-MM-DD hh:mm:ss'}

        self.widget.set_context(context)

class SelectWidget(MyWidget):

    def __init__(self, label, values):
        self.widget = CustomWidget()

        self.widget.set_template_name('main/_widgets/select_widget.html')
        self.widget.set_label(label)

        context = {'values': values}

        self.widget.set_context(context)

class CharWidget(MyWidget):

    #UWAGA zmienne definiowane tu sa STATYCZNE (mozna sie niezle wpuscic w kanal)

    def __init__(self, label):
        self.widget = CustomWidget()

        self.widget.set_template_name('main/_widgets/char_widget.html')
        self.widget.set_label(label)

        print "placeholder: " + label
        context = {'placeholder': label}

        self.widget.set_context(context)

class CheckboxWidget(MyWidget):

    def __init__(self, label):
        self.widget = CustomWidget()

        self.widget.set_template_name('main/_widgets/checkbox_widget.html')
        self.widget.set_label(label)

class TextWidget(MyWidget):

    def __init__(self, label, placeholder, rows):
        self.widget = CustomWidget()

        self.widget.set_template_name('main/_widgets/text_widget.html')
        self.widget.set_label(label)

        context = {'placeholder': placeholder, 'rows': rows}

        self.widget.set_context(context)


def getProjects(Model):

    objects = []

    for m in Model.objects.all():
        objects.append( ( unicode(m.prj_id), m.__unicode__(), "") )

    return objects

def getChoices(Model, fieldName):

    objects = []

    for c in Model._meta.get_field(fieldName).choices:
        objects.append( ( unicode(c[0]), unicode(c[1]), "") )

    return objects

#---------------FORMS---------------#
class SummaryForm(forms.Form):
    rep_redirection = forms.DateTimeField(label = '', required=False, widget = DateWidget("Redirection date").get_widget(), input_formats=['%Y-%m-%d %H:%M:%S'] )
    rep_comment = forms.CharField(label = '', required=False, widget = TextWidget("Comment", '', 3).get_widget() )

    def save(self, report):
        if self.cleaned_data.has_key('rep_redirection'):
            report.rep_redirection = self.cleaned_data['rep_redirection']
        if self.cleaned_data.has_key('rep_comment'):
            report.rep_com_id.com_value = self.cleaned_data['rep_comment']
            report.rep_com_id.save()
        report.save()

class AlertForm(forms.Form):
    alert_project = forms.CharField(label = '', widget = SelectWidget("Project", getProjects(Project) ).get_widget() )
    alert_name = forms.CharField(label = '', widget = CharWidget("Alert name").get_widget() )
    alert_ticket = forms.URLField(label = '', widget = CharWidget("Jira ticket URL").get_widget() )
    alert_type = forms.CharField(label = '', widget = SelectWidget("Alert type", getChoices(Alert, "alt_type")).get_widget() )
    alert_date = forms.DateTimeField(label = '', widget = DateWidget("Alert date").get_widget(), input_formats=['%Y-%m-%d %H:%M:%S'] )
    alert_comment = forms.CharField(label = '', required=False, widget = TextWidget("Comment", '', 3).get_widget() )

    def save(self, report, inc_id=None):
        alert = Alert()
        comment = Comment()
        if self.cleaned_data.has_key('alert_project'):
            alert.alt_prj_id = get_object_or_404(Project, prj_id=self.cleaned_data['alert_project'])
        if self.cleaned_data.has_key('alert_name'):
            alert.alt_name = self.cleaned_data['alert_name']
        if self.cleaned_data.has_key('alert_ticket'):
            alert.alt_ticket = self.cleaned_data['alert_ticket']
        if self.cleaned_data.has_key('alert_date'):
            alert.alt_date = self.cleaned_data['alert_date']
        if self.cleaned_data.has_key('alert_type'):
            alert.alt_type = self.cleaned_data['alert_type']
        if self.cleaned_data.has_key('alert_comment'):
            comment.com_value = self.cleaned_data['alert_comment']

        comment.save()

        alert.alt_com_id = comment
        alert.alt_rep_id = report

        alert.save()

        if inc_id != None:
            incident = Incident.objects.get(inc_id=inc_id)
            incidentStep = IncidentStep()
            incidentStep.ins_type = 'A'
            incidentStep.ins_ent_id = alert.alt_id
            incidentStep.ins_inc_id = incident
            incidentStepComment = Comment()
            incidentStepComment.save()
            incidentStep.ins_com_id = incidentStepComment
            incidentStep.save()

    def modify(self, alt_id):
        alert = Alert.objects.get(alt_id=alt_id)
        comment = Comment.objects.get(com_id=alert.alt_com_id.com_id)

        if self.cleaned_data.has_key('alert_project'):
            alert.alt_prj_id = get_object_or_404(Project, prj_id = self.cleaned_data['alert_project'] )
        if self.cleaned_data.has_key('alert_name'):
            alert.alt_name = self.cleaned_data['alert_name']
        if self.cleaned_data.has_key('alert_ticket'):
            alert.alt_ticket = self.cleaned_data['alert_ticket']
        if self.cleaned_data.has_key('alert_date'):
            alert.alt_date = self.cleaned_data['alert_date']
        if self.cleaned_data.has_key('alert_type'):
            alert.alt_type = self.cleaned_data['alert_type']
        if self.cleaned_data.has_key('alert_comment'):
            comment.com_value = self.cleaned_data['alert_comment']

        comment.save()
        alert.save()


class ContactForm(forms.Form):
    con_prj_id = forms.CharField(label = '', widget = SelectWidget("Project", getProjects(Project) ).get_widget() )
    con_type = forms.CharField(label = '', widget = SelectWidget("Contact type", getChoices(Contact, "con_type")).get_widget())
    con_address = forms.CharField(label = '', widget = CharWidget("Contact address").get_widget() )
    con_direction = forms.CharField(label = '', widget = SelectWidget("Contact direction", getChoices(Contact, "con_direction")).get_widget())
    con_date = forms.DateTimeField(label = '', widget = DateWidget("Contact date").get_widget(), input_formats=['%Y-%m-%d %H:%M:%S'] )
    con_internal = forms.BooleanField(label = '', required=False, widget = CheckboxWidget("Internal").get_widget() )
    con_com_id = forms.CharField(label = '', required=False, widget = TextWidget("Comment", '', 3).get_widget() )

    def save(self, report, inc_id=None):
        contact = Contact()
        comment = Comment()
        print "printuje"
        print self.cleaned_data['con_internal']
        if self.cleaned_data.has_key('con_prj_id'):
            contact.con_prj_id = get_object_or_404(Project, prj_id=self.cleaned_data['con_prj_id'])
        if self.cleaned_data.has_key('con_type'):
            contact.con_type = self.cleaned_data['con_type']
        if self.cleaned_data.has_key('con_address'):
            contact.con_address = self.cleaned_data['con_address']
        if self.cleaned_data.has_key('con_date'):
            contact.con_date = self.cleaned_data['con_date']
        if self.cleaned_data.has_key('con_direction'):
            contact.con_direction = self.cleaned_data['con_direction']
        if self.cleaned_data.has_key('con_internal'):
            contact.con_internal = self.cleaned_data['con_internal']
        if self.cleaned_data.has_key('con_com_id'):
            comment.com_value = self.cleaned_data['con_com_id']

        comment.save()

        contact.con_com_id = comment
        contact.con_rep_id = report

        contact.save()
        if inc_id != None:
            incident = Incident.objects.get(inc_id=inc_id)
            incidentStep = IncidentStep()
            incidentStep.ins_type = 'C'
            incidentStep.ins_ent_id = contact.con_id
            incidentStep.ins_inc_id = incident
            incidentStepComment = Comment()
            incidentStepComment.save()
            incidentStep.ins_com_id = incidentStepComment
            incidentStep.save()

    def modify(self, con_id):
        contact = Contact.objects.get(con_id=con_id)
        comment = Comment.objects.get(com_id=contact.con_com_id.com_id)

        if self.cleaned_data.has_key('con_prj_id'):
            contact.con_prj_id = get_object_or_404(Project, prj_id=self.cleaned_data['con_prj_id'])
        if self.cleaned_data.has_key('con_type'):
            contact.con_type = self.cleaned_data['con_type']
        if self.cleaned_data.has_key('con_address'):
            contact.con_address = self.cleaned_data['con_address']
        if self.cleaned_data.has_key('con_date'):
            contact.con_date = self.cleaned_data['con_date']
        if self.cleaned_data.has_key('con_direction'):
            contact.con_direction = self.cleaned_data['con_direction']
        if self.cleaned_data.has_key('con_internal'):
            contact.con_internal = self.cleaned_data['con_internal']
        if self.cleaned_data.has_key('con_com_id'):
            comment.com_value = self.cleaned_data['con_com_id']

        comment.save()
        contact.save()

class MaintenanceForm(forms.Form):
    mnt_prj_id = forms.CharField(label = '', widget = SelectWidget("Project", getProjects(Project) ).get_widget() )
    mnt_name = forms.CharField(label = '', widget = CharWidget("Maintenance name").get_widget() )
    mnt_date = forms.DateTimeField(label = '', widget = DateWidget("Maintenance date").get_widget(), input_formats=['%Y-%m-%d %H:%M:%S'] )
    mnt_com_id = forms.CharField(label = '', required=False, widget = TextWidget("Comment", '', 3).get_widget() )

    def save(self, report, inc_id=None):
        comment = Comment()
        maintenance = Maintenance()
        if self.cleaned_data.has_key('mnt_prj_id'):
            maintenance.mnt_prj_id = get_object_or_404(Project, prj_id=self.cleaned_data['mnt_prj_id'])
        if self.cleaned_data.has_key('mnt_name'):
            maintenance.mnt_name = self.cleaned_data['mnt_name']
        if self.cleaned_data.has_key('mnt_date'):
            maintenance.mnt_date = self.cleaned_data['mnt_date']
        if self.cleaned_data.has_key('con_com_id'):
            comment.com_value = self.cleaned_data['mnt_com_id']

        comment.save()

        maintenance.mnt_com_id = comment
        maintenance.mnt_rep_id = report

        maintenance.save()
        if inc_id != None:
            incident = Incident.objects.get(inc_id=inc_id)
            incidentStep = IncidentStep()
            incidentStep.ins_type = 'M'
            incidentStep.ins_ent_id = maintenance.mnt_id
            incidentStep.ins_inc_id = incident
            incidentStepComment = Comment()
            incidentStepComment.save()
            incidentStep.ins_com_id = incidentStepComment
            incidentStep.save()

    def modify(self, mnt_id):
        maintenance = Maintenance.objects.get(mnt_id=mnt_id)
        comment = Comment.objects.get(com_id=maintenance.mnt_com_id.com_id)

        if self.cleaned_data.has_key('mnt_prj_id'):
            maintenance.mnt_prj_id = get_object_or_404(Project, prj_id=self.cleaned_data['mnt_prj_id'])
        if self.cleaned_data.has_key('mnt_name'):
            maintenance.mnt_name = self.cleaned_data['mnt_name']
        if self.cleaned_data.has_key('mnt_date'):
            maintenance.mnt_date = self.cleaned_data['mnt_date']
        if self.cleaned_data.has_key('mnt_com_id'):
            comment.com_value = self.cleaned_data['mnt_com_id']

        comment.save()
        maintenance.save()


class IncidentForm(forms.Form):
    inc_prj_id = forms.CharField(label = '', widget = SelectWidget("Project", getProjects(Project) ).get_widget() )
    inc_ticket = forms.URLField(label = '', widget = CharWidget("Jira ticket URL").get_widget() )
    inc_date_start = forms.DateTimeField(label = '', widget = DateWidget("Start date").get_widget(), input_formats=['%Y-%m-%d %H:%M:%S'] )
    inc_date_end = forms.DateTimeField(label = '', required=False, widget = DateWidget("End date").get_widget(), input_formats=['%Y-%m-%d %H:%M:%S'] )
    inc_rca = forms.BooleanField(label = '', required=False, widget = CheckboxWidget("RCA").get_widget() )
    inc_com_id = forms.CharField(label = '', required=False, widget = TextWidget("Comment", '', 3).get_widget() )

    def save(self, report):
        incident = Incident()
        comment = Comment()
        if self.cleaned_data.has_key('inc_prj_id'):
            incident.inc_prj_id = get_object_or_404(Project, prj_id=self.cleaned_data['inc_prj_id'])
        if self.cleaned_data.has_key('inc_ticket'):
            incident.inc_ticket = self.cleaned_data['inc_ticket']
        if self.cleaned_data.has_key('inc_date_start'):
            incident.inc_date_start = self.cleaned_data['inc_date_start']
        if self.cleaned_data.has_key('inc_rca'):
            incident.inc_rca = self.cleaned_data['inc_rca']
        if self.cleaned_data.has_key('inc_com_id'):
            comment.com_value = self.cleaned_data['inc_com_id']


        comment.save()

        incident.inc_com_id = comment
        incident.inc_status = 'O'
        incident.save()

        reportIncident = ReportIncident()
        reportIncident.rpi_inc_id = incident
        reportIncident.rpi_rep_id = report

        reportIncident.save()

    def modify(self, inc_id):
        incident = Incident.objects.get(inc_id=inc_id)
        comment = Comment.objects.get(com_id=incident.inc_com_id.com_id)

        if self.cleaned_data.has_key('inc_prj_id'):
            incident.inc_prj_id = get_object_or_404(Project, prj_id=self.cleaned_data['inc_prj_id'])
        if self.cleaned_data.has_key('inc_ticket'):
            incident.inc_ticket = self.cleaned_data['inc_ticket']
        if self.cleaned_data.has_key('inc_date_start'):
            incident.inc_date_start = self.cleaned_data['inc_date_start']
        if self.cleaned_data.has_key('inc_date_end'):
            incident.inc_date_end = self.cleaned_data['inc_date_end']
        if self.cleaned_data.has_key('inc_com_id'):
            comment.com_value = self.cleaned_data['inc_com_id']

        comment.save()
        incident.save()

class ReportFilterForm(forms.Form):

    rep_id = forms.CharField(label = '', required=False, widget = CharWidget("Id").get_widget() )
    rep_status = forms.CharField(label = '', max_length=1, required=False, widget = CharWidget("Status").get_widget() )
    rep_date_created_from = forms.DateTimeField(label = '', required=False, widget = MinDateWidget("Created from").get_widget(), input_formats=['%Y-%m-%d %H:%M:%S'] )
    rep_date_created_to = forms.DateTimeField(label = '', required=False, widget = MinDateWidget("Created To").get_widget(), input_formats=['%Y-%m-%d %H:%M:%S'] )
    rep_date_sent_from = forms.DateTimeField(label = '', required=False, widget = forms.HiddenInput, input_formats=['%Y-%m-%d %H:%M:%S'] )
    rep_date_sent_to = forms.DateTimeField(label = '', required=False, widget = forms.HiddenInput, input_formats=['%Y-%m-%d %H:%M:%S'] )
    rep_date_removed_from = forms.DateTimeField(label = '', required=False, widget = forms.HiddenInput, input_formats=['%Y-%m-%d %H:%M:%S'] )
    rep_date_removed_to = forms.DateTimeField(label = '', required=False, widget = forms.HiddenInput, input_formats=['%Y-%m-%d %H:%M:%S'] )
    rep_redirection = forms.BooleanField(label = '', required=False, widget = CheckboxWidget("Redirection checked").get_widget() )
    rep_usr_id = forms.CharField(label = '', required=False, widget = CharWidget("User id").get_widget() )

