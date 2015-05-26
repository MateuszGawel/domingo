from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def index(request):
    if request.user.is_authenticated():
        return render(request, 'main/index.html')
    else:
        if request.method == 'POST':
            return __do_login(request)
        else:
            return render(request, 'main/login.html')

def __do_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('main:index')
        else:
            return render(request, 'main/login.html', {'error_message': "Sorry, the account is not active."})
    else:
        return render(request, 'main/login.html', {'error_message': "Please provide correct credentials"})

def do_logout(request):
    logout(request)
    return redirect("main:index")