from django import template

register = template.Library()

@register.filter(is_safe=True)
def urlLastPart(value):
    parts = value.split("/")

    for i in range( len(parts)):
        if len(parts[-i-1]) > 0:
            return parts[-i-1]

    return "Wrong URL"

@register.filter(is_safe=True)
def breadcrumb(value, hostname):
    crumbs = value.split("/")
    crumbs = crumbs[1:-1]

    return __convert_crumbs(crumbs, hostname)

@register.filter(is_safe=True)
def breadcrumb_without_last(value, hostname):
    crumbs = value.split("/")
    crumbs = crumbs[1:-2]

    return __convert_crumbs(crumbs, hostname)


def __convert_crumbs(crumbs, hostname):
    s = '<li><a href="http://' + hostname + '/">main page</a></li> \n'

    for i in range( len(crumbs) ):
        s += '<li'

        if i == len(crumbs) - 1:
            s += ' class="active"> ' + crumbs[i]
        else:
            href = ""

            for j in range(i + 1):
                href += crumbs[j] + '/'

            s += '><a href="http://' + hostname + '/' + href + '" >' + crumbs[i] + '</a>'

        s += ' </li> \n'

    return s

@register.simple_tag
def setSession(request, inc_id):
    if inc_id != None:
        try:
            request.session['inc_id'] = inc_id
        except:
            pass

@register.simple_tag
def clearSession(request):
    try:
        del request.session['inc_id']
    except:
        pass

@register.simple_tag
def checkDisabled(request, report, show=True):

    if request != None and report != None:
        if request.user.is_superuser:
            return "<fieldset>"
        elif report.rep_status == 'O':
            if request.user == report.rep_usr_id:
                return "<fieldset>"
            else:
                if show:
                    return "<div style='color: firebrick; text-align: center; width: 100%'><span style='color: firebrick;' class='glyphicon glyphicon-exclamation-sign'></span> You are not the owner</div> <fieldset disabled>"
                else:
                    return "<fieldset disabled>"
        else:
            if show:
                return "<div style='color: firebrick; text-align: center; width: 100%'><span style='color: firebrick;'class='glyphicon glyphicon-exclamation-sign'></span> The report is not opened</div>  <fieldset disabled>"
            else:
                return "<fieldset disabled>"

    return "<fieldset>"

@register.simple_tag
def disabledButton(request, report):

    if request != None and report != None:
        if request.user.is_superuser:
            return ""
        elif report.rep_status == 'O':
            if request.user == report.rep_usr_id:
                return ""
            else:
                return "disabled"
        else:
            return "disabled"

    return ""
