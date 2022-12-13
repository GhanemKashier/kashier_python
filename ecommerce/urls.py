
from django.contrib import admin
from django.urls import path
from ecom import views
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('webhook',views.webhook,name=''),
    path('show-invoice/<str:pk>',views.show_invoice,name='show-invoice'),
    path('pay',views.pay,name=''),
     path('notification',views.notification,name=''),
     path('',views.admin_view_booking_view,name=''),
 

    path('create-invice', views.create_invice_view,name='create-invice'),

    path('setting', views.admin_products_view,name='setting'),
    path('set_setting', views.set_setting,name=''),
   
    path('list-invoice', views.admin_view_booking_view,name='list-invoices'),
   



]


