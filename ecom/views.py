
# Create your views here.
from django.shortcuts import render,redirect,reverse
# from .models import Product
from ecom.models import Feedback
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

import random
from Kashier import Invoice
import logging


def show_invoice(request,pk):
     MID=request.COOKIES['MID']
     SECRETKEY=request.COOKIES['SECRETKEY']
     APIKEY=request.COOKIES['APIKEY']
     MODE=request.COOKIES['MODE']
     pay=Invoice(MID,APIKEY,MODE,SECRETKEY)
    
    #  pay.get_invoice('INV-3552454483') pay.create_invoice(items,totalAmount,'818895','EGP')
     response=pay.get_invoice(pk) 
     return render(request,'ecom/admin_show_booking.html',{'response':response.json()['response']['data']})

def notification(request):
     MID=request.COOKIES['MID']
     SECRETKEY=request.COOKIES['SECRETKEY']
     APIKEY=request.COOKIES['APIKEY']
     MODE=request.COOKIES['MODE']
     pay=Invoice(MID,APIKEY,MODE,SECRETKEY)
    
     r= pay.share_invoiceByEmail(request.POST.get('email'), request.POST.get('invoice'),  request.POST.get('storename'),request.POST.get('name'))
     r= pay.share_invoiceBySMS(request.POST.get('phone'), request.POST.get('invoice'),  request.POST.get('storename'), request.POST.get('name'))
     return HttpResponse(r)   
    #  pay.get_invoice('INV-3552454483') pay.create_invoice(items,totalAmount,'818895','EGP')
 
    # return redirect ('/admin-view-booking')



def pay(request):
     totalAmount=0
     MID=request.COOKIES['MID']
     SECRETKEY=request.COOKIES['SECRETKEY']
     APIKEY=request.COOKIES['APIKEY']
     MODE=request.COOKIES['MODE']
     pay=Invoice(MID,APIKEY,MODE,SECRETKEY)
    
    # pay.init_item('description',5,10,'itemName',50)
     pay.items.clear()
     for idx, x in enumerate(request.POST.getlist('item_name')): 
       
 
        totalAmount += int(request.POST.getlist('item_qty')[idx]) * float( request.POST.getlist('item_price')[idx])
        pay.init_item(request.POST.getlist('description')[idx],int(request.POST.getlist('item_qty')[idx]),float( request.POST.getlist('item_price')[idx]),request.POST.getlist('item_qty')[idx],float(request.POST.getlist('item_qty')[idx]) * float( request.POST.getlist('item_price')[idx]))
  

  
     respose= pay.create_invoice( pay.items,totalAmount, str(request.POST.get('order_id')),"EGP",0, request.POST.get('dueDate'),  request.POST.get('name')) 
    
    #  respose=pay.share_invoiceByEmail('mghanem@kashier.io','INV-1570812808')
     if(respose.json()['status'] =="FAILURE"):
         return HttpResponse(respose)
     else:    
        # r= pay.share_invoiceByEmail(request.POST.get('email'),  (respose.json()['response']['paymentRequestId']),  __package__, str(request.user))
        # r= pay.share_invoiceBySMS(request.POST.get('phone'),  (respose.json()['response']['paymentRequestId']),  __package__, str(request.user))
        return render(request,'ecom/view_feedback.html',{'storename':request.POST.get('name'), 'storename':request.POST.get('storename'),'email':request.POST.get('email'),'phone':request.POST.get('phone'),'invoice':respose.json()['response']['paymentRequestId']})
    #   return HttpResponse(r.json()['status'])
  




# admin view customer table
def create_invice_view(request):
    
    return render(request,'ecom/payment.html')



# admin view the product
def admin_products_view(request):
  
   if 'MID' in request.COOKIES:
      MID=request.COOKIES['MID']
      SECRETKEY=request.COOKIES['SECRETKEY']
      APIKEY=request.COOKIES['APIKEY']
      MODE=request.COOKIES['MODE']

      return render(request,'ecom/admin_products.html',{'MID':MID,'SECRETKEY':SECRETKEY,'APIKEY':APIKEY,'MODE':MODE})
   MID='null'
   return render(request,'ecom/admin_products.html',{'MID':MID})

# admin add product by clicking on floating button
def set_setting(request):
   response= HttpResponseRedirect('setting')
   response.set_cookie('MID',request.POST.get('MID'))
   response.set_cookie('APIKEY',request.POST.get('APIKEY'))
   response.set_cookie('SECRETKEY',request.POST.get('SECRETKEY'))
   response.set_cookie('MODE',request.POST.get('MODE'))
   
   request.session['MID'] =request.POST.get('MID')
   request.session['APIKEY'] =request.POST.get('APIKEY')
   request.session['SECRETKEY'] =request.POST.get('SECRETKEY')
   request.session['MODE'] =request.POST.get('MODE')
   logger = logging.getLogger(__name__)
   logger.critical("-----------------------------"+ request.session['APIKEY'])
   return  response





def admin_view_booking_view(request):
    pay=Invoice('MID-15708-128','032d694a-fdab-4096-8d52-c06f5475d9ce','test',"7f73d9d7fe4688a48831c25888cd7256$b1c8356554111fdecc6fd484f510ff521740c6ba15a3f7752358adbf6f9c200ede50f71c37e088911dc4f440975764db")
    response=pay.get_list_invoices(1,30)
   
   # return HttpResponse(response.json()['response']['data'])
    return render(request,'ecom/admin_view_booking.html',{'response':response.json()['response']['data']})



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

     MID=request.session.get('MID','MID-15708-128')
     SECRETKEY=request.session.get('SECRETKEY','7f73d9d7fe4688a48831c25888cd7256$b1c8356554111fdecc6fd484f510ff521740c6ba15a3f7752358adbf6f9c200ede50f71c37e088911dc4f440975764db')
     APIKEY=request.session.get('APIKEY','d4ff74df-972c-4e3f-ba56-3df994a0f41c')
     MODE=request.session.get('MODE','test')
     logger.critical("-----------------------------"+MODE)

     pay=Invoice(MID,APIKEY,MODE,SECRETKEY)
        
     payload = request.body
    #
     data=json.loads(payload)
     logger.critical(data)

     logger.critical(request.headers.get('x-kashier-signature'))
     logger.critical(pay.verify_webhook(request))
     back= Feedback.objects.create(name=pay.verify_webhook(request),feedback=data)
     logger.critical("-------back----------------")
     
     return HttpResponse(pay.verify_webhook(request)) 
