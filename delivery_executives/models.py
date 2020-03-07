from django.db import models
from contracts.models import Contracts
from datetime import datetime
import json
import pyqrcode
from wasche.custom_settings import settings
# Create your models here.
class Deliver_Executive(models.Model):
    
    name = models.CharField(max_length=100,default="")
    contract_name = models.ForeignKey(Contracts,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20,default="")
    address = models.CharField(max_length=254,default="")
    qr_code_data = models.BinaryField()    
    date_joined = models.DateTimeField(editable=False)
    
    def save(self,*args,**kwargs):
        if not self.id:
            self.date_joined = datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
        # de = Deliver_Executive.objects.all().order_by("-id")
        # if len(de)==0:
        #     i = 1
        
        # qr = pyqrcode.create(json.dumps({"wasche-services":{"name":self.name,"id":self.id}}))
        # dta = "data:image/png;base64," + qr.png_as_base64_str()
        # self.qr_code_data = bytes(dta,'utf-8')
        return super(Deliver_Executive,self).save(*args,**kwargs)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Delivery Exceutive Details"


class ongoing_delivery(models.Model):
    name = models.ForeignKey(Deliver_Executive,on_delete=models.CASCADE)
    on_going = models.CharField(max_length=24,default="")
    date_started = models.DateTimeField(editable=False)
    
    def save(self,*args,**kwargs):
        if not self.id:
            self.date_started = datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
        return super(ongoing_delivery,self).save(*args,**kwargs)
    
    def __str__(self):
        return self.name.name

    class Meta:
        verbose_name_plural = "Ongoing Delivery Details"
    