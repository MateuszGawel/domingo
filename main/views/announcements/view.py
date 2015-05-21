from django.shortcuts import render


def index(request):
    if request.user.is_authenticated():
        return render(request, 'main/announcements/index.html')
    else:
        return render(request, 'main/login.html', None)