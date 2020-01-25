from django.db import models
# from django.utils import timezone
from datetime import datetime
from wasche.custom_settings import settings
# Create your models here.
class Contracts(models.Model):
    contract_name = models.CharField(max_length=254,primary_key=True,unique=True)
    contract_address = models.CharField(max_length = 254)
    contract_phone_number = models.CharField(max_length = 20)
    contract_zip_code = models.CharField(max_length = 15)
    contract_country = models.CharField(max_length=100)
    contract_state = models.CharField(max_length = 100)
    contract_established_date = models.DateTimeField(editable=False)

    def save(self,*args,**kwargs):
        
        self.contract_established_date = datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
        return super(Contracts,self).save(*args,**kwargs)
    def __str__(self):
        return self.contract_name

    class Meta:
        verbose_name_plural = "Contracts"
    