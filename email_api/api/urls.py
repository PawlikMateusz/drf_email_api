from django.urls import path, include
from rest_framework import routers

from .views import MailboxViewSet, EmailViewSet, TemplateViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register('mailbox', MailboxViewSet)
router.register('template', TemplateViewSet)
router.register('email', EmailViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
