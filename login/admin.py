from django.contrib import admin
from login.models import User,ConfirmString,Region

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(ConfirmString)
class ConfirmStringAdmin(admin.ModelAdmin):
    pass

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass
