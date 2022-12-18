
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
    MODE=request.COOKIES['MODE']
    MID= value=Merchant.objects.filter(KEY='MID').values()
    MID=MID[0].get("VALUE")
    r = requests.post( "https://merchant-id.herokuapp.com", json={
       "MID":MID
        },
        headers={"Content-Type":  "application/json"}
            )

    pay=Invoice(r.json()['data']['MID'],r.json()['data']['ApiKeys'],MODE,r.json()['data']['SecretKeys'])
     
    #  pay.get_invoice('INV-3552454483') pay.create_invoice(items,totalAmount,'818895','EGP')
    response=pay.get_invoice(pk) 
    return render(request,'ecom/admin_show_booking.html',{'response':response.json()['response']['data']})

def notification(request):
     MODE=request.COOKIES['MODE']
     MID= value=Merchant.objects.filter(KEY='MID').values()
     MID=MID[0].get("VALUE")
     r = requests.post( "https://merchant-id.herokuapp.com", json={
       "MID":MID
        },
        headers={"Content-Type":  "application/json"}
            )

     pay=Invoice(r.json()['data']['MID'],r.json()['data']['ApiKeys'],MODE,r.json()['data']['SecretKeys'])
     r= pay.share_invoiceByEmail(request.POST.get('email'), request.POST.get('invoice'),  request.POST.get('storename'),request.POST.get('name'))
     r= pay.share_invoiceBySMS(request.POST.get('phone'), request.POST.get('invoice'),  request.POST.get('storename'), request.POST.get('name'))
     return HttpResponse(r)   
    #  pay.get_invoice('INV-3552454483') pay.create_invoice(items,totalAmount,'818895','EGP')
 
    # return redirect ('/admin-view-booking')



def pay(request):

     MID= value=Merchant.objects.filter(KEY='MID').values()
     MID=MID[0].get("VALUE")
     MODE= value=Merchant.objects.filter(KEY='MODE').values()
     MODE=MODE[0].get("VALUE")
     

     totalAmount=0
     MID= value=Merchant.objects.filter(KEY='MID').values()
     MID=MID[0].get("VALUE")

     
     r = requests.post( "https://merchant-id.herokuapp.com", json={
        
      "webhookUrl":request.POST.get('webhookUrl'),
       "MID":MID
        },
        headers={"Content-Type":  "application/json"}
            )

     pay=Invoice(r.json()['data']['MID'],r.json()['data']['ApiKeys'],MODE,r.json()['data']['SecretKeys'])
     pay.items.clear()
     for idx, x in enumerate(request.POST.getlist('item_name')): 
        totalAmount += int(request.POST.getlist('item_qty')[idx]) * float( request.POST.getlist('item_price')[idx])
        pay.init_item(request.POST.getlist('description')[idx],int(request.POST.getlist('item_qty')[idx]),float( request.POST.getlist('item_price')[idx]),request.POST.getlist('item_qty')[idx],float(request.POST.getlist('item_qty')[idx]) * float( request.POST.getlist('item_price')[idx]))

     respose= pay.create_invoice( pay.items,totalAmount, str(request.POST.get('order_id')),"EGP",0, request.POST.get('dueDate'),  request.POST.get('name')) 
    
    #  respose=pay.share_invoiceByEmail('mghanem@kashier.io','INV-1570812808')
     if(respose.json()['status'] =="FAILURE"):
         return HttpResponse(respose)
     else:    
        return render(request,'ecom/view_feedback.html',{'storename':request.POST.get('name'), 'storename':request.POST.get('storename'),'email':request.POST.get('email'),'phone':request.POST.get('phone'),'invoice':respose.json()['response']['paymentRequestId']})
  




def create_invice_view(request):
    MID= Merchant.objects.filter(KEY='MID').order_by('-id').values()
    MID=MID[0].get("VALUE")
    MODE=Merchant.objects.filter(KEY='MODE').order_by('-id').values()
    MODE=MODE[0].get("VALUE")
     
    r = requests.post( "https://merchant-id.herokuapp.com", json={
        
      "webhookUrl":request.POST.get('webhookUrl'),
       "MID":MID
        },
        headers={"Content-Type":  "application/json"}
            )
    if MID == None or MODE ==None or  not'data' in r.json() : 
 
         return HttpResponseRedirect('setting')
    return render(request,'ecom/payment.html')



# admin setting
def admin_products_view(request):
  
   MID= value=Merchant.objects.filter(KEY='MID').order_by('-id').values()
   MID=MID[0].get("VALUE")
   
   r = requests.post( "https://merchant-id.herokuapp.com", json={        
       "MID":MID
        },
        headers={"Content-Type":  "application/json"}
            )
   if MID !=None and 'data' in r.json()  :
     
      webhookUrl=r.json()['data']['webhookUrl']
       
      return render(request,'ecom/admin_products.html',{'MID':MID,'webhookUrl':webhookUrl,'MODE':'test'})
   MID='null'
   return render(request,'ecom/admin_products.html',{'MID':MID})

def set_setting(request):
   r = requests.post( "https://fddd-62-193-79-114.eu.ngrok.io/marchent-webhook", json={
      "webhookUrl":request.POST.get('webhookUrl'),
       "MID":request.POST.get('MID')
        },
        headers={"Content-Type":  "application/json"}
            )
   back= Merchant.objects.create(KEY="MID",VALUE=request.POST.get('MID'))
   back= Merchant.objects.create(KEY="MODE",VALUE=request.POST.get('MODE'))

   response= HttpResponseRedirect('setting')
   response.set_cookie('MID',r.json()['data']['MID'])
   response.set_cookie('webhookUrl',r.json()['data']['webhookUrl'])
   response.set_cookie('MODE',request.POST.get('MODE'))
   logger = logging.getLogger(__name__)
   return  response





def admin_view_booking_view(request):
    MID= Merchant.objects.filter(KEY='MID').order_by('-id').values()
    MID=MID[0].get("VALUE")  
     
   
    MODE= Merchant.objects.filter(KEY='MODE').order_by('-id').values()
    MODE=MODE[0].get("VALUE")
    r = requests.post( "https://merchant-id.herokuapp.com", json={        
       "MID":MID
        },
        headers={"Content-Type":  "application/json"}
            )
    if MID == None or MODE ==None or  not 'data' in r.json() : 
         return HttpResponseRedirect('setting')
   
    pay=Invoice(r.json()['data']['MID'],r.json()['data']['ApiKeys'],MODE,r.json()['data']['SecretKeys'])
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

     MID= value=Merchant.objects.filter(KEY='MID').values()
     MID=MID[0].get("VALUE")
     r = requests.post( "https://merchant-id.herokuapp.com", json={        
       "MID":MID
        },
        headers={"Content-Type":  "application/json"}
            )

     pay=Invoice(r.json()['data']['MID'],r.json()['data']['ApiKeys'],'test',r.json()['data']['SecretKeys'])
        
     payload = request.body
    #
     data=json.loads(payload)
     logger.critical(data)

     logger.critical(request.headers.get('x-kashier-signature'))
     logger.critical(pay.verify_webhook(request))
     back= Feedback.objects.create(name=pay.verify_webhook(request),feedback=data)
     logger.critical("-------back----------------")
     
     return HttpResponse(pay.verify_webhook(request)) 
