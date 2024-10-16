from django.contrib import admin
from .models import LogEntry


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'timestamp', 'http_method', 'uri', 'response_code', 'response_size')
    list_filter = ('ip_address', 'http_method', 'response_code')
    search_fields = ('uri',)
