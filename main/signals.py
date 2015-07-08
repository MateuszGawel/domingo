import django.dispatch

new_report_signal = django.dispatch.Signal(providing_args=["message"])