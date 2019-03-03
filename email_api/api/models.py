from django.db import models
from django.contrib.postgres.fields import ArrayField

import uuid
# Create your models here.


class Mailbox(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.CharField(max_length=100)
    port = models.IntegerField(default=465)
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email_from = models.CharField(max_length=50)
    use_ssl = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    @property
    def sent(self):
        return Email.objects.filter(mailbox=self).count()

    def __str__(self):
        return self.host


class Template(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField(max_length=200)
    text = models.TextField()
    attachment = models.FileField(
        upload_to='attachments', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class Email(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mailbox = models.ForeignKey(
        'Mailbox', on_delete=models.PROTECT, related_name='emails')
    template = models.ForeignKey(
        'Template', on_delete=models.PROTECT, related_name='emails')
    to = ArrayField(models.EmailField(), blank=False)
    cc = ArrayField(models.EmailField(), blank=True, null=True)
    bcc = ArrayField(models.EmailField(), blank=True, null=True)
    reply_to = models.EmailField(blank=True, null=True)
    send_date = models.DateTimeField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.to)
