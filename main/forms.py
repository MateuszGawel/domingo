from django import forms
from django.forms import ModelForm
from main.models import *
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.utils.encoding import smart_text, force_str, force_text

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

        self.widget.set_template_name('main/widgets/date_widget.html')
        self.widget.set_label(label)

        context = {'placeholder': 'YYYY-MM-DD hh:mm:ss'}

        self.widget.set_context(context)

class SelectWidget(MyWidget):

    def __init__(self, label, values):
        self.widget = CustomWidget()

        self.widget.set_template_name('main/widgets/select_widget.html')
        self.widget.set_label(label)

        context = {'values': values}

        self.widget.set_context(context)

class CharWidget(MyWidget):

    #UWAGA zmienne definiowane tu sa STATYCZNE (mozna sie niezle wpuscic w kanal)

    def __init__(self, label):
        self.widget = CustomWidget()

        self.widget.set_template_name('main/widgets/char_widget.html')
        self.widget.set_label(label)

        context = {'placeholder': label}

        self.widget.set_context(context)

class CheckboxWidget(MyWidget):

    def __init__(self, label):
        self.widget = CustomWidget()

        self.widget.set_template_name('main/widgets/checkbox_widget.html')
        self.widget.set_label(label)

class TextWidget(MyWidget):

    def __init__(self, label, placeholder, rows):
        self.widget = CustomWidget()

        self.widget.set_template_name('main/widgets/text_widget.html')
        self.widget.set_label(label)

        context = {'placeholder': placeholder, 'rows': rows}

        self.widget.set_context(context)


def getModelObjects(Model):

    objects = []

    for m in Model.objects.all():
        objects.append( ( unicode(m.prj_id), m.__unicode__()) )

    return objects


class AlertForm(forms.Form):

    alert_project = forms.CharField(label = '', widget = SelectWidget("Project", getModelObjects(Project) ).get_widget() )
    alert_name = forms.CharField(label = '', widget = CharWidget("Alert name").get_widget() )
    alert_ticket = forms.CharField(label = '', widget = CharWidget("Jira ticket URL").get_widget() )
    alert_date = forms.CharField(label = '', widget = DateWidget("Alert date").get_widget() )
    alert_type = forms.CharField(label = '', widget = SelectWidget("Alert type", Alert._meta.get_field('alt_type').choices).get_widget() )
    #your_choose = forms.BooleanField(label = '', widget = CheckboxWidget("Jakis checkbox").get_widget() )
    alert_comment = forms.CharField(label = '', widget = CharWidget("Comment").get_widget() ) # widget = TextWidget("Comment", "Enter here your comment", 5).get_widget() )


class NameForm(forms.Form):

    print [0][0] # .alt_type.get_ .choices
    print "tyle"

    your_name = forms.CharField(label='', max_length=100, widget = CharWidget("CHAR").get_widget())
    your_date = forms.CharField(label = '', widget = DateWidget("DUPA").get_widget() )
    your_select = forms.ChoiceField(label = '', widget = SelectWidget("cos", Alert._meta.get_field('alt_type').choices).get_widget() )
    your_choose = forms.BooleanField(label = '', widget = CheckboxWidget("Jakis checkbox").get_widget() )
