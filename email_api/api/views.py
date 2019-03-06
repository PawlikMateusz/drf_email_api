from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .tasks import send_email
from .models import Email, Mailbox, Template
from .serializers import EmailSerializer, TemplateSerializer, MailboxSerializer


class MailboxViewSet(viewsets.ModelViewSet):
    queryset = Mailbox.objects.all()
    serializer_class = MailboxSerializer


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer


class EmailFilter(filters.FilterSet):
    sent = filters.BooleanFilter(
        field_name='send_date', lookup_expr='isnull', exclude=True)

    class Meta:
        model = Email
        fields = ['send_date', 'date']


class EmailViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EmailFilter

    def create(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            mailbox = get_object_or_404(Mailbox, id=request.data['mailbox'])
            if mailbox.is_active:
                send_email.apply_async(
                    (request.data, serializer.instance.id), retry=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"Error": "Selected mailbox is not active"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
