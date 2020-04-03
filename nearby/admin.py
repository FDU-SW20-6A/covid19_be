from django.contrib import admin
from nearby.models import city,pois

@admin.register(city)
class cityAdmin(admin.ModelAdmin):
    pass

@admin.register(pois)
class poisAdmin(admin.ModelAdmin):
    pass

