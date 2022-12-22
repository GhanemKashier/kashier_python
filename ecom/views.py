
# Create your views here.
from django.shortcuts import render,redirect,reverse
# from .models import Product
from ecom.models import Feedback,Merchant
# from ecom.forms import AddressForm,ContactusForm,CustomerForm,CustomerUserForm,FeedbackForm,OrderForm,ProductForm,User
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
import json 
from datetime import datetime
import requests
import random
from Kashier import Invoice
import logging


def show_invoice(request,pk):
    MID=Merchant.objects.filter(KEY='MID').order_by('-id').values()
  
    if not MID[0]:
       return HttpResponseRedirect('setting')
    MID=MID[0].get("VALUE")
    secretKey=Merchant.objects.filter(KEY='secretKey').order_by('-id').values()
    if not secretKey:
       
     return HttpResponseRedirect('setting')
    secretKey=secretKey[0].get("VALUE")
    webhookUrl=Merchant.objects.filter(KEY='webhookUrl').order_by('-id').values()
    if webhookUrl:
        webhookUrl=webhookUrl[0].get("VALUE")
    settings= Invoice(MID,secretKey)
    pay= Invoice(MID,secretKey)
    
    response=pay.get_invoice(pk) 
    # return HttpResponse(response)

    return render(request,'ecom/admin_show_booking.html',{'response':response.json()['response']['data']})

def notification(request):
    
     MID= Merchant.objects.filter(KEY='MID').order_by('-id').values() 
     MID=MID[0].get("VALUE")
     MODE= value=Merchant.objects.filter(KEY='MODE').values()
     MODE=MODE[0].get("VALUE")
  
     secretKey=Merchant.objects.filter(KEY='secretKey').order_by('-id').values()
     if secretKey:
       secretKey=secretKey[0].get("VALUE")  

     pay=Invoice(MID,secretKey ,MODE,)  
     r= pay.share_invoiceByEmail(request.POST.get('email'), request.POST.get('invoice'),  request.POST.get('storename'),request.POST.get('name'))
     r= pay.share_invoiceBySMS(request.POST.get('phone'), request.POST.get('invoice'),  request.POST.get('storename'), request.POST.get('name'))
     return HttpResponse(r)   
    #  pay.get_invoice('INV-3552454483') pay.create_invoice(items,totalAmount,'818895','EGP')
 
    # return redirect ('/admin-view-booking')



def pay(request):

     MID= Merchant.objects.filter(KEY='MID').order_by('-id').values() 
     MID=MID[0].get("VALUE")
     MODE= value=Merchant.objects.filter(KEY='MODE').values()
     MODE=MODE[0].get("VALUE")
     totalAmount=0
     secretKey=Merchant.objects.filter(KEY='secretKey').order_by('-id').values()
     if secretKey:
       secretKey=secretKey[0].get("VALUE")  

     pay=Invoice(MID,secretKey ,MODE,)
     pay.items.clear()
     for idx, x in enumerate(request.POST.getlist('item_name')): 
        totalAmount += int(request.POST.getlist('item_qty')[idx]) * float( request.POST.getlist('item_price')[idx])
        pay.init_item(request.POST.getlist('description')[idx],int(request.POST.getlist('item_qty')[idx]),float( request.POST.getlist('item_price')[idx]),request.POST.getlist('item_qty')[idx],float(request.POST.getlist('item_qty')[idx]) * float( request.POST.getlist('item_price')[idx]))

     respose= pay.create_invoice( pay.items,totalAmount, str(request.POST.get('order_id')),"EGP",0, request.POST.get('dueDate'),  request.POST.get('name')) 
    #  respose=pay.share_invoiceByEmail('mghanem@kashier.io','INV-1570812808')
     if(respose['status'] =="FAILURE"):
         return HttpResponse(respose['messages']['ar'])
     else:    
        return render(request,'ecom/view_feedback.html',{'storename':request.POST.get('name'), 'storename':request.POST.get('storename'),'email':request.POST.get('email'),'phone':request.POST.get('phone'),'invoice':respose['response']['paymentRequestId']})
  




def create_invice_view(request):
    MID= Merchant.objects.filter(KEY='MID').order_by('-id').values()
   
            
    if not MID  : 
 
         return HttpResponseRedirect('setting')
    return render(request,'ecom/payment.html')



# admin setting
def admin_products_view(request):
  
   MID=Merchant.objects.filter(KEY='MID').order_by('-id').values()
   MID=MID[0].get("VALUE")
   secretKey=Merchant.objects.filter(KEY='secretKey').order_by('-id').values()
   if secretKey:
       secretKey=secretKey[0].get("VALUE")
   webhookUrl=Merchant.objects.filter(KEY='webhookUrl').order_by('-id').values()
   if webhookUrl:
        webhookUrl=webhookUrl[0].get("VALUE")
   settings= Invoice(MID,secretKey)
   merchant=settings.merchant()
   if MID !=None and merchant != False  :
      
    #   webhookUrl=merchant['data']['webhookUrl']
    #   secretKey=merchant['data']['secret']

       
      return render(request,'ecom/admin_products.html',{'MID':MID,'webhookUrl':webhookUrl,'MODE':'test','secretKey':secretKey})
  
   return render(request,'ecom/admin_products.html',{'MID':MID,'webhookUrl':'','MODE':' ' ,'secretKey':''})

def set_setting(request):
  
   back= Merchant.objects.create(KEY="MID",VALUE=request.POST.get('MID'))
   back= Merchant.objects.create(KEY="MODE",VALUE=request.POST.get('MODE'))
   back= Merchant.objects.create(KEY="secretKey",VALUE=request.POST.get('secretKey'))
   settings= Invoice(request.POST.get('MID'),request.POST.get('secretKey'))
   result=settings.set_webhook(request.POST.get('webhookUrl'))
   if result:
          back= Merchant.objects.create(KEY="webhookUrl",VALUE=request.POST.get('webhookUrl'))

   response= HttpResponseRedirect('setting')
   
   logger = logging.getLogger(__name__)
   return  response





def admin_view_booking_view(request):
    
    MID=Merchant.objects.filter(KEY='MID').order_by('-id').values()
  
    if not MID[0]:
       return HttpResponseRedirect('setting')
    MID=MID[0].get("VALUE")
    secretKey=Merchant.objects.filter(KEY='secretKey').order_by('-id').values()
    if not secretKey:
       
     return HttpResponseRedirect('setting')
    secretKey=secretKey[0].get("VALUE")
    webhookUrl=Merchant.objects.filter(KEY='webhookUrl').order_by('-id').values()
    if webhookUrl:
        webhookUrl=webhookUrl[0].get("VALUE")
    settings= Invoice(MID,secretKey)
    pay= Invoice(MID,secretKey)
    
    response=pay.get_list_invoices(1,30)
    
   # return HttpResponse(response.json()['response']['data'])
    return render(request,'ecom/admin_view_booking.html',{'response':response['response']['data']})



# admin view the feedback
def view_feedback_view(request):
    feedbacks= Feedback.objects.all().order_by('-id')
    return render(request,'ecom/view_feedback.html',{'feedbacks':feedbacks})




@csrf_exempt
def customer_address_view(request):
  
    # if there is no product in cart we will not show address form
    logger = logging.getLogger(__name__)
    return render(request,'ecom/payment.html')


@csrf_exempt
def my_order_view(request):

    return render(request,'ecom/payment.html')

@csrf_exempt
def webhook(request):
     logger = logging.getLogger(__name__)
     MID=Merchant.objects.filter(KEY='MID').order_by('-id').values()
     MID=MID[0].get("VALUE")
     secretKey=Merchant.objects.filter(KEY='secretKey').order_by('-id').values()
     if secretKey:
       secretKey=secretKey[0].get("VALUE")
     webhookUrl=Merchant.objects.filter(KEY='webhookUrl').order_by('-id').values()
     if webhookUrl:
        webhookUrl=webhookUrl[0].get("VALUE")
     pay= Invoice(MID,secretKey)
    
     payload = request.body
    #
     data=json.loads(payload)
     logger.critical(data)

     logger.critical(request.headers.get('x-kashier-signature'))
     logger.critical(pay.verify_webhook(request))
     back= Feedback.objects.create(name=pay.verify_webhook(request),feedback=data)
     logger.critical("-------back----------------")
     
     return HttpResponse(pay.verify_webhook(request)) 
