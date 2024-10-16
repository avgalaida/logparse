from rest_framework import serializers
from .models import LogEntry


class LogEntrySerializer(serializers.ModelSerializer):
    ip_address = serializers.IPAddressField(help_text="IP-адрес клиента.")
    timestamp = serializers.DateTimeField(help_text="Дата и время запроса.")
    http_method = serializers.CharField(max_length=10, help_text="HTTP-метод запроса (GET, POST и т.д.).")
    uri = serializers.CharField(max_length=200, help_text="URI запрошенного ресурса.")
    response_code = serializers.IntegerField(help_text="Код ответа сервера.")
    response_size = serializers.IntegerField(help_text="Размер ответа в байтах.")

    class Meta:
        model = LogEntry
        fields = '__all__'
