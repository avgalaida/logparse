from django.db import models


class LogEntry(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField()
    http_method = models.CharField(max_length=10)
    uri = models.CharField(max_length=200)
    response_code = models.IntegerField()
    response_size = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['ip_address']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['response_code']),
        ]

    def __str__(self):
        return f"{self.ip_address} - {self.uri}"
