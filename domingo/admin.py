from django.contrib import admin

from domingo.models import Alert, Call, Duty, Project, Report


admin.site.register(Alert)
admin.site.register(Call)
admin.site.register(Duty)
admin.site.register(Project)
admin.site.register(Report)