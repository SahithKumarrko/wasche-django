from django.db import models
# from django.utils import timezone
from datetime import datetime
from wasche.custom_settings import settings
from user.models import User
import json
from dashboard.models import Order_DashBoard

# Create your models here.
class Tracker(models.Model):
    track_id = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.CharField(max_length=24,default="No Date Provided")
    time = models.CharField(max_length=24,default="No Time Provided")
    on_going = models.BooleanField(default=True)
    # type_op = models.CharField(max_length="50",default="")
    completed_status = models.CharField(max_length=50,default="")
    # operation = models.CharField(max_length=254,default="")
    ordered_data = models.CharField(max_length=254,default="")
    created_date = models.DateTimeField(editable=False)
    def __str__(self):
        return self.track_id.email

    def save(self,*args,**kwargs):
        if not self.id:
            self.created_date = datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
            o = Order_DashBoard.objects.get(email = self.track_id)
            dates = o.process_ordered_dates(self.ordered_data)
            self.date = dates["date"]
            self.time= dates["time"]
        return super(Tracker,self).save(*args,**kwargs)

    class Meta:
        verbose_name_plural = "Tracker Details"
    
    def update_operation(self,data):
        
        d = self.get_data()
        d[data["type"]] = data["data"]
        self.ordered_data = json.dumps(d)
    def update_completion(self,data):
        if data == "s":
            self.completed_status = "success"
            self.on_going = False
        else:
            self.completed_status = "failed"
            self.on_going=False
        o = Order_DashBoard.objects.get(email=self.track_id)
        o.update_dashboard(self.date,self.time,data)
        o.save()
    def get_data(self):
        return json.loads(self.ordered_data)
        