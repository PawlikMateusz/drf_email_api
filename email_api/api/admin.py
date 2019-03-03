from django.contrib import admin

from .models import Email, Mailbox, Template
# Register your models here.
admin.site.register(Email)
admin.site.register(Mailbox)
admin.site.register(Template)
