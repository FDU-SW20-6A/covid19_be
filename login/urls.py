from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.login),
    path('register/',views.register),
    path('logout/',views.logout),
    path('current/',views.getCurrentUser),
    path('subscribe/get/',views.getSubscribe),
    path('subscribe/add/',views.addSubscribe),
    path('subscribe/delete/',views.delSubscribe),
    path('weekly/get/',views.getWeekly),
    #path('input/',views.inputdata),
    #path('confirm/',views.userConfirm),
    ]
