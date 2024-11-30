from django.contrib import admin

from .models import AuthCode, User

admin.site.register(AuthCode)
admin.site.register(User)
