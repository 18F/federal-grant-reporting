from django.contrib import admin
from .models import Finding, Agency, Grant, Grantee, User

admin.site.register(User)
admin.site.register(Agency)
admin.site.register(Finding)
admin.site.register(Grant)
admin.site.register(Grantee)
