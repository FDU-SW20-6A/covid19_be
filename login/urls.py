from django.urls import path
from . import views
urlpatterns = [
    path('index/',views.index),
    path('login/',views.login),
    path('register/',views.register),
    path('logout/',views.logout),
    path('confirm/',views.userConfirm),
    ]
