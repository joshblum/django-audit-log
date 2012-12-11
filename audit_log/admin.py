from django.db import models

from django.contrib import admin

import time
import datetime
import re

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

    def action_date_friendly(self, obj):
        return '%s UTC' %str(obj.action_date.strftime('%m/%d/%y %I:%M:%S'))

    def action_user_friendly(self, obj):
        user = obj.action_user
        search_by_user = '<a href="%s">%s</a>' % (user, user)
        return search_by_user

    def action_type_friendly(self, obj):
        # if there's an easier way to extract it from 
        # models.CharField in managers, I would use that instead.
        # For now, just copied the codes here
        types = {
            'I': 'Created',
            'U': 'Changed',
            'D': 'Deleted',
            'G': 'Read'
        }
        return types[obj.action_type]

    def action_ip_friendly(self, obj):
        ip = obj.action_ip
        search_by_ip = '<a href="?q=%s">%s</a>' % (ip, ip)
        return search_by_ip
    
    def action_referrer_friendly(self, obj):
        return obj.action_referrer

    def action_user_agent_friendly(self, obj):
        print obj.action_user_agent
        regex = re.compile("\((.*?)\)", re.IGNORECASE)
        r = regex.search(str(obj.action_user_agent))
        res = None
        if r.groups():
            res = r.groups()[0]
        return res
    
    def action_get_params_friendly(self, obj):
        return obj.action_get_params

    def action_post_params_friendly(self, obj):
        return obj.action_post_params

    def action_request_url_friendly(self, obj):
        return obj.action_request_url

    action_date_friendly.allow_tags = True
    action_date_friendly.short_description = 'Timestamp'
    
    action_user_friendly.allow_tags = True
    action_user_friendly.short_description = 'User'

    action_type_friendly.short_description = 'Type'
    
    action_ip_friendly.allow_tags = True
    action_ip_friendly.short_description = 'IP Address'

    action_request_url_friendly.short_description = 'URL'
    action_user_agent_friendly.short_description = 'User Agent'
    action_get_params_friendly.short_description = 'GET'
    action_post_params_friendly.short_description = 'POST'
        
    list_display = ('action_user_friendly', 'action_type_friendly', 'action_ip_friendly', 'action_request_url_friendly', 'action_user_agent_friendly', 'action_get_params_friendly', 'action_post_params_friendly', 'action_date_friendly')

    list_display_links = ('action_date_friendly',)

    search_fields = ('action_user__username', 'action_referrer', 'action_ip', 'action_date', 'action_user_agent', 'action_request_url', 'action_get_params', 'action_post_params',)
    list_filter = ('action_type',)
    ordering = ['-action_date']

reg_admin()
