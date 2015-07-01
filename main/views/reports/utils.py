from django.db import connections

from main.forms import *

def get_data_from_jira(query):
    '''Zwraca kursor na ktorym trzeba wykonac odpowiednia metode by pobrac dane. Np fetchone()'''
    cursor = connections['jira'].cursor()
    cursor.execute(query)
    return cursor

def doValidate(form=None, request=None, report=None, incident=None):

    if request != None and report != None:
        if request.user.is_superuser:
            print "super"
        elif report.rep_status == 'O':
            if request.user == report.rep_usr_id:
                print "is owner"
            else:
                print "not open!"
                return False
        else:
            print "not super!"
            return False

    if form == None:
        print "no form!"
        return False
    else:
        return form.is_valid()