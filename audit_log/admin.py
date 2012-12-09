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

    def action_id_friendly(self, obj):
        return obj.action_id

    def action_date_friendly(self, obj):
        return '<b>'+str(obj.action_date.strftime('%m/%d/%y %I:%M:%S')) + ' UTC</b>'

    def action_user_friendly(self, obj):
        search_by_user = '<a href="?q=%s">%s</a>' % (obj.action_user, obj.action_user)
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
        search_by_ip = '<a href="?q=%s">%s</a>' % (obj.action_ip, obj.action_ip)
        return search_by_ip
    
    def action_referrer_friendly(self, obj):
        return obj.action_referrer

    def action_user_agent_friendly(self, obj):
        regex = re.compile("\((.*?)\)", re.IGNORECASE)
        r = regex.search(str(obj.action_user_agent))
        res = None
        if r.groups():
            res = r.groups()[0]
        return res

    action_id_friendly.short_description = 'ID'

    action_date_friendly.allow_tags = True
    action_date_friendly.short_description = 'Timestamp'
    
    action_user_friendly.allow_tags = True
    action_user_friendly.short_description = 'User'

    action_type_friendly.short_description = 'Type'
    
    action_ip_friendly.allow_tags = True
    action_ip_friendly.short_description = 'IP Address'

    action_referrer_friendly.short_description = 'Referrer'

    action_user_agent_friendly.short_description = 'User Agent'
        
    list_display = ('action_id_friendly', 'action_user_friendly', 'action_type_friendly', 'action_ip_friendly', 'action_referrer_friendly', 'action_user_agent_friendly', 'action_date_friendly')

    list_display_links = ('action_id_friendly', 'action_date_friendly')

    search_fields = ('action_user__username', 'action_referrer', 'action_ip', 'action_date', 'action_user_agent')
    list_filter = ('action_type',)
    ordering = ['action_id']

reg_admin()
