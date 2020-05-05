from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.login),
    path('register/',views.register),
    path('logout/',views.logout),
    path('subscribe/get/',views.getSubscribe),
    path('subscribe/add/',views.addSubscribe),
    path('subscribe/delete/',views.delSubscribe),
    #path('input/',views.inputdata),
    #path('confirm/',views.userConfirm),
    ]
