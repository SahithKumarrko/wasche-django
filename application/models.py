from django.db import models
# from django.utils import timezone
from datetime import datetime
from wasche.custom_settings import settings
# Create your models here.
from user.views import User

class Contact(models.Model):
    name = models.CharField(max_length=254)
    email = models.EmailField(default="")
    subject = models.CharField(max_length = 254)
    message = models.CharField(max_length = 1000)
    date_sent = models.DateTimeField(editable=False)
    def __str__(self):
        return "From : ( " + self.name + "), Email : ( " + self.email + " )"

    class Meta:
        verbose_name_plural = "Contacts"
    
    def save(self,*args,**kwargs):
        if not self.id:
            self.date_sent = datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
        return super(Contact,self).save(*args,**kwargs)


class Subscribers(models.Model):
    email = models.EmailField()
    date_subscribed = models.DateTimeField(editable=False)
    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Subscribers"
    
    def save(self,*args,**kwargs):
        if not self.id:
            self.date_subscribed = datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
        return super(Subscribers,self).save(*args,**kwargs)

class Plans(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    plan = models.CharField(max_length=254,default="None")
    date_created = models.DateTimeField(editable=False)
    extra_amount = models.FloatField(default=0.0)
    end_date = models.DateTimeField(editable=False)
    remaining_amount = models.FloatField(default=0.0)
    eligibility = models.CharField(max_length = 400,default = "")
    notified = models.BooleanField(default = False)
    current_order_id = models.CharField(max_length=254,default="")
    regular_count = models.IntegerField(default=0)
    other_count = models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = "Plans"
    def __str__(self):
        return self.user.email +"   :  " + self.plan

    def save(self,*args,**kwargs):
        if not self.id:
            self.date_created = datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
            self.end_date = self.date_created
        return super(Plans,self).save(*args,**kwargs)

    