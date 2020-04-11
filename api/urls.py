from django.urls import path
from . import views
urlpatterns = [
    path('sina_api/',views.sina_api),
    path('province/',views.province),
    path('country/',views.country),
    path('overall_China/',views.overall_China),
    path('overall_world/',views.overall_world),
    path('province_list/',views.province_list),
    path('country_list/',views.country_list),
    path('history_China/',views.history_China),
    path('history_world/',views.history_world),
    path('rate/',views.rate),
    ]
    