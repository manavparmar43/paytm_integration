from django.contrib import admin
from paytm_app.models import Transaction,Shiping
# Register your models here.
@admin.register(Transaction)
class Transactions(admin.ModelAdmin):
        list_display=['id','shiping_detail','is_payment','amount','order_id','checksum','date_time']

@admin.register(Shiping)
class Shiping_Detail(admin.ModelAdmin):
        list_display=['id','product_name','product_description','product_price','name','user','city','state','address']