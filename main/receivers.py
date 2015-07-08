import django.dispatch
from django.dispatch import receiver
from signals import new_report_signal
from django.core.signals import request_finished
from django.shortcuts import redirect

request = None

@receiver(new_report_signal)
def my_handler(sender, **kwargs):
    print("DOSTALEM SIGNALA!!!!")
    print sender

# @receiver(request_finished)
# def my_callback(sender, **kwargs):
#     global request
#     request = sender.request_class._get_request()