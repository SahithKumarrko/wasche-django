from django.db import models
from django.utils import timezone
# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=254)
    email = models.EmailField(default="")
    subject = models.CharField(max_length = 254)
    message = models.CharField(max_length = 1000)
    date_sent = models.DateTimeField(editable=False)
    class Meta:
        verbose_name_plural = "Contacts"
    
    def save(self,*args,**kwargs):
        if not self.id:
            self.date_sent = timezone.now()
        return super(Contact,self).save(*args,**kwargs)


class Subscribers(models.Model):
    email = models.EmailField()
    date_subscribed = models.DateTimeField(editable=False)
    class Meta:
        verbose_name_plural = "Subscribers"
    
    def save(self,*args,**kwargs):
        if not self.id:
            self.date_subscribed = timezone.now()
        return super(Subscribers,self).save(*args,**kwargs)
