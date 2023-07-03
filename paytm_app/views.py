from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from  paytm_app.models import Shiping,Transaction
from .checksum import generate_checksumx ,verify_checksum
from django.views.decorators.csrf import csrf_exempt
import hashlib
import json
# Create your views here.
import uuid
from django.conf import settings


class Login (View):
    def get(self,request):
        return render(request,'login.html')

class Shoping(View):
    def get(self,request):
        return render(request,'shoping.html')
    
class ShipingView(View):
    def get(self,request):
        return render(request,'shiping_detail.html')
    def post(self,request):
        user=User.objects.get(username=request.POST['username'])
        shiping=Shiping.objects.create(product_name=request.POST['product_name'],product_description=request.POST['product_description'],
                                       product_price=request.POST['product_price'],name=request.POST['first_name']+' '+ request.POST['last_name'], 
                                       city=request.POST['city'],user=user,state=request.POST['state'],address=request.POST['address'])
        shiping.save()
        unicode=uuid.uuid1().hex
        payment=Transaction.objects.create(shiping_detail=shiping,amount=request.POST['product_price'],order_id=unicode)
        payment.save()
        merchant_key = settings.PAYTM_SECRET_KEY
        param_dict={

            'MID': settings.PAYTM_MERCHANT_ID,
            'ORDER_ID': payment.order_id,
            'CUST_ID': request.user.email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'TXN_AMOUNT': str(request.POST['product_price']),
            'CALLBACK_URL':'http://127.0.0.1:8001/handlerequest/',

        }
        # paytm_params = dict(param_dict)
        param_dict['CHECKSUMHASH'] = generate_checksum(param_dict, merchant_key)
        print(param_dict)
        payment.checksum = param_dict['CHECKSUMHASH']
        payment.save()
        return  render(request, 'payment.html', {'param_dict': param_dict})
        # return render(request, 'your_app/checkout.html')

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    print("hy")
    form = request.POST
    print(form)
    response_dict = {}
    for i in form.keys():
        print(i,"><><><><><><><><><>")
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = verify_checksum(response_dict, settings.PAYTM_MERCHANT_ID,response_dict['CHECKSUMHASH'])
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'callback.html', {'response': response_dict})