from django.shortcuts import render
from main.forms import *
from django import forms

def get_current_report(request):
    report = Report.objects.filter(rep_usr_id=request.user.id, rep_date_sent=None).latest('rep_id')
    return report

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
    from django.db import load_backend
    myBackend = load_backend('django.db.backends.oracle')
    myConnection = myBackend.DatabaseWrapper(
        {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'JIRA',
        'USER': 'jiranew',
        'PASSWORD': 'jiraqq',
        'HOST': '10.233.12.7',
        'PORT': '1521',
        'OPTIONS': {},
        'CONN_MAX_AGE': 1200,
        'AUTOCOMMIT': False
    })

    myCursor = myConnection.cursor()
    myCursor.execute(query)
    return myCursor