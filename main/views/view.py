from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib.auth.models import User
import string
import random


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

        user = None

        try:
            user = User.objects.get(username=username)
        except Exception:
            return render(request, 'main/login.html', {'error_message': "User " + username + " does not exist!"})

        return render(request, 'main/login.html', {'error_message': "Wrong password - <a href='"+reverse("main:reset_password", kwargs={'username': username})+"'>reset for " + username + "</a>", "user_to_reset": username})

def do_logout(request):
    logout(request)
    return redirect("main:index")

def reset_password(request, username):
    new_password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))

    user = User.objects.get(username=username)
    user.set_password(new_password)
    user.save()

    #receiver = [user.email]
    receiver = ['michal.antkowicz@comarch.pl']

    send_mail('Domingo password reset', 'Hi ' + username + ', your new password is: ' + new_password, 'noreply@domingo.com', receiver, fail_silently=False)
    return render(request, 'main/login.html', {'error_message': "The new password has been sent to " + username + "!"})