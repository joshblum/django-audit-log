from django.db import models

from django.contrib import admin

def reg_admin():
    for model in models.get_models():
        if _check_name(model):
            admin.site.register(model, DefaultAuditAdmin)

def _check_name(cls):
    return "AuditLogEntry" in cls.__name__

class DefaultAuditAdmin(admin.ModelAdmin):
    """
        Generic admin interface for displaying audit objects
    """
    pass

reg_admin()