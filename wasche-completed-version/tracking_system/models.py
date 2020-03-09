from django.db import models
# from django.utils import timezone
from datetime import datetime
from datetime import timedelta
from wasche.custom_settings import settings
from user.models import User
import json
from dashboard.models import Order_DashBoard

class Tracker(models.Model):
    track_id = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.CharField(max_length=24,default="No Date Provided")
    time = models.CharField(max_length=24,default="No Time Provided")
    on_going = models.BooleanField(default=True)
    type_op = models.CharField(max_length=50,default="")
    completed_status = models.CharField(max_length=500,default="")
    # operation = models.CharField(max_length=254,default="")
    completion_date = models.DateTimeField(editable=False)
    created_date = models.DateTimeField(editable=False)
    def __str__(self):
        return self.track_id.email

    def save(self,*args,**kwargs):
        if not self.id:
            # self.created_date = datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
            # o = Order_DashBoard.objects.get(email = self.track_id)
            # dates = o.process_ordered_dates()
            # self.date = dates["date"]
            # self.time= dates["time"]
            self.type_op="co"
            self.completed_status = json.dumps({"co":str(self.created_date.strftime("%Y-%m-%d %H:%M:%S %p"))})
            self.completion_date = self.created_date + timedelta(seconds=110000)
        return super(Tracker,self).save(*args,**kwargs)

    class Meta:
        verbose_name_plural = "Tracker Details"
    
    def update_operation(self,data):
        
        d = self.get_data()
        d[data["type"]] = str(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"))
        self.completed_status = json.dumps(d)
        if data["type"]=="pd":
            self.on_going=False
        self.type_op = data["type"]
    # def update_completion(self,data):
    #     d = self.get_data()
    #     if data == "s":
    #         d["pd"] = 
    #         self.on_going = False
    #     else:
    #         self.completed_status = "failed"
    #         self.on_going=False
    #     o = Order_DashBoard.objects.get(email=self.track_id)
    #     o.update_dashboard(self.date,self.time,data)
    #     o.save()
    def get_data(self):
        return json.loads(self.completed_status)
        