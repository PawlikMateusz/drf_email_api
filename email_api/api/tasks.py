from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from django.core.mail import EmailMessage, get_connection
from django.shortcuts import get_object_or_404
from django.utils import timezone


import logging
from datetime import datetime
from smtplib import SMTPException

from email_api.celery import app
from .models import Email, Mailbox, Template

logger = logging.getLogger('api')


def create_message(data, email):
    mailbox = get_object_or_404(Mailbox, id=data['mailbox'])
    template = get_object_or_404(Template, id=data['template'])
    connection = get_connection(host=mailbox.host,
                                port=mailbox.port,
                                username=mailbox.login,
                                password=mailbox.password,
                                use_tls=mailbox.use_ssl)
    message = EmailMessage(
        subject=template.subject,
        body=template.text,
        from_email=mailbox.email_from,
        to=data['to'],
        cc=email.cc,
        bcc=email.bcc,
        reply_to=email.reply_to,
        headers={'Message-ID': 'Custom email id'},
        connection=connection
    )
    if template.attachment:
        message.attach_file(template.attachment.path)
    return message


@app.task(bind=True, default_retry_delay=3, max_retries=3,)
def send_email(self, data, email_id):
    email = get_object_or_404(Email, id=email_id)
    message = create_message(data, email)
    try:
        message.send()
    except SMTPException:
        try:
            self.retry()
        except MaxRetriesExceededError:
            logger.debug(
                "Email sending failed from mailbox, more information:")
            logger.debug("------mailbox id: '{0}'".format(data['mailbox']))
            logger.debug("------email id: '{0}'".format(email.id))
    else:
        logger.debug(
            "Email send successfully, email id: '{0}'".format(email.id))
        email.send_date = datetime.now(tz=timezone.utc)
        email.save()
