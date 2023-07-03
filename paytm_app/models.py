from django.db import models
from django.contrib.auth.models import User


# Create your models here.



class Shiping(models.Model):
    product_name=models.CharField(max_length=100,blank=True,null=True)
    product_description=models.TextField()
    product_price=models.CharField(max_length=20,blank=True,null=True)
    name=models.CharField(max_length=200,blank=True,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    city=models.CharField(max_length=200,blank=True,null=True)
    state=models.CharField(max_length=100,blank=True,null=True)
    address=models.TextField()

    def __str__(self) :
        return self.name
    
class Transaction(models.Model):
    shiping_detail=models.ForeignKey(Shiping,on_delete=models.CASCADE, blank=True,null=True)
    amount=models.CharField(max_length=15,blank=True,null=True)
    is_payment=models.BooleanField(default=False)
    order_id=models.CharField(max_length=20,blank=True,null=True)
    checksum=models.CharField(max_length=50,blank=True,null=True)
    date_time=models.DateTimeField(auto_now_add=True)
    def __str__(self) :
        return self.shiping_detail.user.first_name +' '+ self.shiping_detail.user.first_name



