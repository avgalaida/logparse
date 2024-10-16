from django.urls import path, include
from rest_framework import routers
from .views import LogEntryViewSet

router = routers.DefaultRouter()
router.register(r'logentries', LogEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
