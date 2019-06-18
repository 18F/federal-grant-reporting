from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Finding, Agency, Grant, Grantee, User

admin.site.register(User, UserAdmin)
admin.site.register(Agency)
admin.site.register(Finding)
admin.site.register(Grant)
admin.site.register(Grantee)
