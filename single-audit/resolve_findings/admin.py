from django.contrib import admin
from .models import Finding, Agency, Grant, Grantee, Comment

admin.site.register(Agency)
admin.site.register(Finding)
admin.site.register(Grant)
admin.site.register(Grantee)
admin.site.register(Comment)
