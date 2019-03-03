from rest_framework import serializers

from .models import Email, Template, Mailbox


class MailboxSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(initial=False)
    use_ssl = serializers.BooleanField(initial=True)

    class Meta:
        model = Mailbox
        fields = ('id', 'host', 'port', 'login', 'password', 'email_from',
                  'use_ssl', 'is_active', 'date', 'last_update', 'sent')


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ('id', 'subject', 'text', 'attachment', 'date', 'last_update')


class EmailSerializer(serializers.ModelSerializer):
    send_date = serializers.DateTimeField(read_only=True, initial=None)

    def validate_to(self, to):
        if not to:
            raise serializers.ValidationError('This field is required')
        return to

    class Meta:
        model = Email
        fields = ('id', 'mailbox', 'template', 'to', 'cc', 'bcc',
                  'reply_to', 'send_date', 'date')
