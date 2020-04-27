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
    path('history/',views.history),
    path('rate/',views.rate),
    path('continent/',views.continent),
    path('scatter_diagram/',views.scatter_diagram),
    path('news/',views.news),
    path('rumor0/',views.rumor0),
    path('rumor2/',views.rumor2),
    path('country_history/',views.country_history),
    path('province_history/',views.province_history),
    ]
    