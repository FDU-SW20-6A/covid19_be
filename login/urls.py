from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.login),
    path('register/',views.register),
    path('logout/',views.logout),
    path('current/',views.getCurrentUser),
    path('change/',views.changePassword),
    path('reset/',views.resetPassword),
    path('subscribe/get/',views.getSubscribe),
    path('subscribe/post/',views.postSubscribe),
    path('weekly/get/',views.getWeekly),
    path('confirm/',views.userConfirm),
    ]
