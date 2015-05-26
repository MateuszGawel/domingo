from django.db import connections

from main.forms import *


def get_current_report(request):
    report = Report.objects.filter(rep_usr_id=request.user.id, rep_date_sent=None).latest('rep_id')
    return report

def get_inner_tuple_index(baseTuple, element):
    '''Potrzebne zeby wziac index wewnetrznego tuple'a z choices modelu - nie bedzie potrzebne jesli zamiast tego choices typy alertow itp wrzucimy do tabel'''
    for i in range( len(baseTuple) ):
        if element in baseTuple[i]:
            return i
        else:
            print "nie znalazlem ", element, " w ", baseTuple[i], " | a index to ", i
    return -1

def check_csrf(request):
    if request.method == 'POST':
        form = forms.Form(request.POST)
        if form.is_valid():
            return True
    return False

def get_data_from_jira(query):
    '''Zwraca kursor na ktorym trzeba wykonac odpowiednia metode by pobrac dane. Np fetchone()'''
    cursor = connections['jira'].cursor()
    cursor.execute(query)
    return cursor