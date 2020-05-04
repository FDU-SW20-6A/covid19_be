from django.contrib import admin
from login.models import User,ConfirmString

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(ConfirmString)
class ConfirmStringAdmin(admin.ModelAdmin):
    pass
