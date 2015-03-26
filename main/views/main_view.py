from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from main.views import report_view
from main.models import Report

def index(request):
    if request.user.is_authenticated():
        report = Report.objects.filter(rep_usr_id=request.user.id)
        if report.exists():
            report = report.latest('rep_id')
        else:
            report = None
        return render(request, 'main/index.html', {'report': report})
    else:
        return render(request, 'main/login.html', None)

def do_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return render(request, 'main/index.html', None)
        else:
            return render(request, 'main/login.html', {'error_message': "Sorry, the account is not active."})
    else:
        return render(request, 'main/login.html', {'error_message': "Please provide correct credentials"})

def do_logout(request):
    logout(request)
    return render(request, 'main/login.html', {'error_message': "Thanks for logging out. Now you can login again.", "error_type": "success"})