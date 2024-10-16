from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import LogEntry
from .serializers import LogEntrySerializer
from rest_framework.pagination import LimitOffsetPagination
from drf_yasg.utils import swagger_auto_schema


class LogEntryViewSet(viewsets.ModelViewSet):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ip_address', 'response_code', 'http_method']
    search_fields = ['uri']
    ordering_fields = ['timestamp', 'response_size']
    pagination_class = LimitOffsetPagination

    @swagger_auto_schema(
        operation_summary="Получить список лог-записей",
        operation_description="Возвращает список лог-записей с поддержкой фильтрации, поиска и пагинации."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить лог-запись по ID",
        operation_description="Возвращает лог-запись по указанному ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать новую лог-запись",
        operation_description="Создает новую лог-запись."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить лог-запись",
        operation_description="Обновляет существующую лог-запись."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление лог-записи",
        operation_description="Частично обновляет существующую лог-запись."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить лог-запись",
        operation_description="Удаляет лог-запись."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)