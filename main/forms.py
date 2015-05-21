from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

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

        context = {'placeholder': 'YYYY-MM-DD hh:mm:ss'}

        self.widget.set_context(context)

class SelectWidget(MyWidget):

    def __init__(self, label, values):
        self.widget = CustomWidget()

        self.widget.set_template_name('main/_widgets/select_widget.html')
        self.widget.set_label(label)

        context = {'values': values}

        self.widget.set_context(context)

    def dupa(self):
        print "COKOLWIEK"

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
        objects.append( (c[0], c[1], "") )

    return objects

class SummaryForm(forms.Form):
    rep_redirection = forms.DateTimeField(label = '', required=False, widget = DateWidget("Redirection date").get_widget(), input_formats=['%Y-%m-%d %H:%M:%S'] )
    rep_comment = forms.CharField(label = '', required=False, widget = TextWidget("Comment", '', 3).get_widget() )

class AlertForm(forms.Form):

    alert_project = forms.CharField(label = '', widget = SelectWidget("Project", getProjects(Project) ).get_widget() )
    alert_name = forms.CharField(label = '', widget = CharWidget("Alert name").get_widget() )
    alert_ticket = forms.URLField(label = '', widget = CharWidget("Jira ticket URL").get_widget() )
    alert_type = forms.CharField(label = '', widget = SelectWidget("Alert type", getChoices(Alert, "alt_type")).get_widget() )
    alert_date = forms.DateTimeField(label = '', widget = DateWidget("Alert date").get_widget(), input_formats=['%Y-%m-%d %H:%M:%S'] )
    alert_comment = forms.CharField(label = '', required=False, widget = TextWidget("Comment", '', 3).get_widget() )

class ContactForm(forms.Form):

    con_prj_id = forms.CharField(label = '', widget = SelectWidget("Project", getProjects(Project) ).get_widget() )
    con_type = forms.CharField(label = '', widget = SelectWidget("Contact type", getChoices(Contact, "con_type")).get_widget())
    con_address = forms.CharField(label = '', widget = CharWidget("Contact address").get_widget() )
    con_direction = forms.CharField(label = '', widget = SelectWidget("Contact direction", getChoices(Contact, "con_direction")).get_widget())
    con_date = forms.DateTimeField(label = '', widget = DateWidget("Contact date").get_widget(), input_formats=['%Y-%m-%d %H:%M:%S'] )
    con_internal = forms.BooleanField(label = '', required=False, widget = CheckboxWidget("Internal").get_widget() )
    con_com_id = forms.CharField(label = '', required=False, widget = TextWidget("Comment", '', 3).get_widget() )

class MaintenanceForm(forms.Form):

    mnt_prj_id = forms.CharField(label = '', widget = SelectWidget("Project", getProjects(Project) ).get_widget() )
    mnt_name = forms.CharField(label = '', widget = CharWidget("Maintenance name").get_widget() )
    mnt_date = forms.DateTimeField(label = '', widget = DateWidget("Maintenance date").get_widget(), input_formats=['%Y-%m-%d %H:%M:%S'] )
    mnt_com_id = forms.CharField(label = '', required=False, widget = TextWidget("Comment", '', 3).get_widget() )

class IncidentForm(forms.Form):

    inc_prj_id = forms.CharField(label = '', widget = SelectWidget("Project", getProjects(Project) ).get_widget() )
    inc_ticket = forms.URLField(label = '', widget = CharWidget("Jira ticket URL").get_widget() )
    inc_date_start = forms.DateTimeField(label = '', widget = DateWidget("Start date").get_widget(), input_formats=['%Y-%m-%d %H:%M:%S'] )
    inc_date_end = forms.DateTimeField(label = '', required=False, widget = DateWidget("End date").get_widget(), input_formats=['%Y-%m-%d %H:%M:%S'] )
    inc_com_id = forms.CharField(label = '', required=False, widget = TextWidget("Comment", '', 3).get_widget() )

class ReportFilterForm(forms.Form):

    rep_id = forms.CharField(label = '', required=False, widget = CharWidget("Id").get_widget() )
    rep_status = forms.CharField(label = '', max_length=1, required=False, widget = CharWidget("Status").get_widget() )
    rep_date_created_from = forms.DateTimeField(label = '', required=False, widget = DateWidget("Created date from").get_widget(), input_formats=['%Y-%m-%d %H:%M:%S'] )
    rep_date_created_to = forms.DateTimeField(label = '', required=False, widget = DateWidget("Created date to").get_widget(), input_formats=['%Y-%m-%d %H:%M:%S'] )
    rep_date_sent_from = forms.DateTimeField(label = '', required=False, widget = DateWidget("Sent date from").get_widget(), input_formats=['%Y-%m-%d %H:%M:%S'] )
    rep_date_sent_to = forms.DateTimeField(label = '', required=False, widget = DateWidget("Sent date to").get_widget(), input_formats=['%Y-%m-%d %H:%M:%S'] )
    rep_date_removed_from = forms.DateTimeField(label = '', required=False, widget = DateWidget("Removed date from").get_widget(), input_formats=['%Y-%m-%d %H:%M:%S'] )
    rep_date_removed_to = forms.DateTimeField(label = '', required=False, widget = DateWidget("Removed date to").get_widget(), input_formats=['%Y-%m-%d %H:%M:%S'] )
    rep_redirection = forms.BooleanField(label = '', required=False, widget = CheckboxWidget("Redirection checked").get_widget() )
    rep_usr_id = forms.CharField(label = '', required=False, widget = CharWidget("User id").get_widget() )

class NameForm(forms.Form):

    your_name = forms.CharField(label='', max_length=100, widget = CharWidget("CHAR").get_widget())
    your_date = forms.CharField(label = '', widget = DateWidget("DUPA").get_widget() )
    your_select = forms.ChoiceField(label = '', widget = SelectWidget("cos", Alert._meta.get_field('alt_type').choices).get_widget() )
    your_choose = forms.BooleanField(label = '', widget = CheckboxWidget("Jakis checkbox").get_widget() )
