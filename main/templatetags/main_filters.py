from django import template

register = template.Library()

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
    s = '<li><a href="http://' + hostname + '/">Main page</a></li> \n'

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
