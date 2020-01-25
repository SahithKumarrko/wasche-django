from django.db import models
# from django.utils import timezone
from datetime import datetime
from wasche.custom_settings import settings
from user.models import User

# Create your models here.
class Transaction(models.Model):
    order_id = models.AutoField(primary_key=True)
    
    customer_email = models.ForeignKey(User,on_delete=models.CASCADE)

    customer_name = models.CharField(max_length=254,default="No Name Provided")
    customer_phone_number = models.CharField(max_length=20,default="")
    # type_op = models.CharField(max_length="50",default="")
    # operation = models.CharField(max_length=254,default="")
    plan = models.CharField(max_length=50,default="")
    amount = models.CharField(max_length=10,default="")
    referenceId = models.CharField(max_length=260,default="")
    completed_status = models.BooleanField(default=False)
    eligibility = models.CharField(max_length=400,default="")
    transaction_date = models.DateTimeField(editable=False)

    def __str__(self):
        return self.customer_email.email

    def save(self,*args,**kwargs):
        if not self.order_id:
            print("creating transaction")
            self.transaction_date = datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
            
        return super(Transaction,self).save(*args,**kwargs)

    class Meta:
        verbose_name_plural = "Transaction Details"
    