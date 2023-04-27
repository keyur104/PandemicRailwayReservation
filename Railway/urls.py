
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path('',views.instruction,name="instruction"),
    path('index',views.index,name="index"),
    path('afterSearch',views.afterSearch,name="afterSearch"),
    path('seatAlloc',views.seatAlloc,name="seatAlloc"),
    path('registration', views.registration, name = 'registration'),
    path('afterregistration',views.afterregistration, name = 'afterregistration'),
    path('checkAvail',views.checkAvail, name = 'checkAvail'), 
    path("signup", views.signup, name='signup'),
    path("afterlogin",views.afterlogin, name='afterlogin'),
    path("aftersignup",views.aftersignup, name='aftersignup'),
    path("login", views.login, name='login'),
    path("medical", views.medical, name='medical'),
    path("history", views.history, name='history'),   
    path("pendingmedical", views.pendingmedical, name='pendingmedical'),
    path("logout", views.logout, name='logout'),
    path("ticket", views.ticket, name='ticket'),
    path("cancelticket", views.cancelticket, name='cancelticket'),
    path("aftercancel", views.aftercancel, name='aftercancel'),
]

urlpatterns=urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


