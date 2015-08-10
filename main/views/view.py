from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.core.mail import send_mail


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
        return render(request, 'main/login.html', {'error_message': "Incorrect credentials (<a href='"+reverse("main:reset_password")+"'>reset password</a>)"})

def do_logout(request):
    logout(request)
    return redirect("main:index")

def reset_password(request):
    send_mail('Subject here', 'Here is the message.', 'from@example.com', ['michal.antkowicz@comarch.pl'], fail_silently=False)
    return render(request, 'main/login.html', {'error_message': "The new password has been sent to you!"})