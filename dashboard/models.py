from django.db import models
from user.models import User
# from django.utils import timezone
import json
from datetime import datetime
from wasche.custom_settings import settings
# Create your models here.

# class Overflown_Orders_Data(models.Model):
#     email = models.ForeignKey(User,on_delete=models.CASCADE)
#     overflown_data = models.CharField(max_length = 20100,default="")
#     date_created = models.DateTimeField(editable=False)

#     class Meta:
#         verbose_name_plural = "Overflown Orders Data"
#     def save(self, *args, **kwargs):
#         if not self.id:
#             self.date_created = datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
#         return super(Overflown_Orders_Data,self).save(*args,**kwargs)


class Old_Orders(models.Model):
    email = models.ForeignKey(User,on_delete=models.CASCADE)
    data = models.CharField(max_length = 20100,default="")
    date_created = models.DateTimeField(editable=False)
    # years = models.CharField(max_length=20,default="")
    def __str__(self):
        return self.email.email

    class Meta:
        verbose_name_plural = "Old data of orders"
    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
        return super(Old_Orders,self).save(*args,**kwargs)

class Order_DashBoard(models.Model):
    email = models.OneToOneField(User,on_delete=models.CASCADE)
    # current_week = models.CharField(max_length=254,default="")
    # monthly = models.CharField(max_length=254,default="")
    # current_month = models.CharField(max_length=254,default="")
    # month_weekly = models.CharField(max_length=1000,default="")
    total_orders = models.CharField(max_length=254,default="0")
    ordered_dates = models.CharField(max_length=20000,default="")
    # overflown_ordered_dates = models.CharField(max_length=21000,default="")
    overflown = models.BooleanField(default=False)
    recent_date = models.CharField(max_length=24,default="")
    recent_time = models.CharField(max_length=24,default="")
    # current_date = models.DateTimeField()
    years = models.CharField(max_length=150,default="")
    date_created = models.DateTimeField(editable = False)
    def __str__(self):
        return self.email.email

    class Meta:
        verbose_name_plural = "Order DashBoards"
    def save(self, *args, **kwargs):
        date = datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
        # ood = Overflown_Orders_Data(email=self.email,overflown_data=self.ordered_dates)
        # ood.save()
            
        if not self.id:
            print("Created new date for user")
            self.date_created = date

        # self.current_date = date
        # if len(self.ordered_dates)>=20000 or self.overflown:
        #     ood = Overflown_Orders_Data(email=self.email,overflown_data=self.ordered_dates)
        #     ood.save()
        #     # self.overflown_ordered_dates = self.ordered_dates
        #     self.ordered_dates=""
        #     print("overflown")
        if self.ordered_dates=="":
            print("From order_dashboard in models : Initializing ordered_dates")
            y_m = str(date).split()[0].split("-")
            self.years = json.dumps([y_m[0]])
            if y_m[1][0]=='0':
                y_m[1] = "".join(list(y_m[1])[1:])
            self.ordered_dates = json.dumps({y_m[0]:{y_m[1][0]:{}}})
        
        return super(Order_DashBoard,self).save(*args,**kwargs)
    
    def process_ordered_dates(self,clothes_ordered,new_order=False,old_order=False):
        date = datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
        # from calendar import monthrange
        d_t = date
        date_order = str(date).split()[1].split(".")[0]
        date = str(date).split()[0].split("-")
        cur = self.get_ordered_date()
        ly = list(cur.keys())[0]
        # if len(cur[ly].keys)==0:
        #     cur[ly]
        # noo = {}
        self.total_orders = str( int(self.total_orders) + 1 )
        if date[1][0]=='0':
            date[1] = "".join(list(date[1])[1:])
        if date[2][0]=='0':
            date[2] = "".join(list(date[2])[1:])
            
        if (int(date[0]) > int(ly)):
            print("year ended")
            old_data = Old_Orders(email=self.email,data=json.dumps(cur))
            old_data.save()
            a = json.loads(self.years)
            a = a.append(date[0])
            self.years = json.dumps(a)
            del cur[ly]
            
            cur[date[0]] = {date[1] : { date[2] : { date_order : clothes_ordered } } }
            # cur[date[0]][date[1]] = 
        elif len(cur[ly].keys())==0:
            cur[ly][date[1]] = { date[2] : { date_order : clothes_ordered } } 

        else:
            lm = list(cur[ly].keys())[-1]

            if lm != date[1]:
                print("no matching month")
                cur[ly][date[1]] = {date[2]:{ date_order : clothes_ordered}}

            else:
                print(list(cur[ly][lm].keys()))
                print(date[2])
                print(date[2] in list(cur[ly][lm].keys()))
                if date[2] in list(cur[ly][lm].keys()):
                    print("date found")
                    # if new_order:
                    #     cur[ly][lm][date[2]] = clothes_ordered
                    # if old_order:
                    cur[ly][lm][date[2]][date_order] = clothes_ordered
                    # if type(cur[ly][lm][date[2]]) == int:
                    #     cur[ly][lm][date[2]] = [cur[ly][lm][date[2]]]
                    # cur[ly][lm][date[2]].append(cur[ly][lm][date[2]][-1] +  clothes_ordered)
                else:
                    cur[ly][lm][date[2]] = { date_order : clothes_ordered}
                # self.ordered_dates = json.dumps(cur)
        self.ordered_dates = json.dumps(cur)
        
        # print("Order dates  :   ",cur)
        
        data = json.dumps(cur)
        if ly==date[0] and len(data)>=19999:
            ood = Old_Orders(email=self.email,data=data)
            ood.save()
            # self.overflown_ordered_dates = self.ordered_dates
            self.ordered_dates=json.dumps({date[0]:{date[1]:{}}})
            self.overflown = True
            print("overflown")
        
        dat = {"date":str(d_t).split()[0],"time":str(d_t).split()[1].split(".")[0]}
        self.recent_date = dat["date"]
        self.recent_time = dat["time"]
        self.save()
        from tracking_system.models import Tracker
        t = Tracker(track_id = self.email,date = self.recent_date,time = self.recent_time,created_date = d_t)
        t.save()
        return dat
        # return {"year":ly,"orders":cur}
    def update_dashboard(self,date,time,update_data):
        date_order = time
        date = date.split("-")
        date[1] = str(int(date[1]))
        date[2] = str(int(date[2]))
        
        print("Date  :  ",date)
        cur = self.get_ordered_date()
        ly = date[0]
        lm = date[1]
        if date[2] in list(cur[ly][lm].keys()):
            print("date found")
            # from application.models import Plans
            # if new_order:
            #     cur[ly][lm][date[2]] = clothes_ordered
            # if old_order:
            categ = ["Inner Wear","Upper Wear","Lower Wear","Other"]
            cur[ly][lm][date[2]][date_order] = update_data
            # print("\n\n\nModified  Cur  : ",cur,"\n\n")
            tot = 0
            for i in update_data.keys():
                if i in categ:
                    tot = tot + int(update_data[i])
            if self.email.plans.plan != "None":
                
                rem = settings.regular_count[self.email.plans.plan] - (self.email.plans.regular_count + tot)
                print(tot,rem)
                if rem<0:
                    tot = tot - abs(rem)
                    self.email.plans.other_count = self.email.plans.other_count + rem

                self.email.plans.regular_count = self.email.plans.regular_count + tot
                self.email.plans.save()
            else:
                self.email.plans.other_count = self.email.plans.other_count + tot
                self.email.plans.save()

            self.ordered_dates = json.dumps(cur)
            self.save()
            # print("\n\nupdated data   :  ",self.ordered_dates)
            return "Modified"
        else:
            return "Problem Modifying data"
        # if len(cur[ly])==12:
        #     if len(cur)==31:
        #         print("year ended")
        #         return
        # lm = cur[list(cur[ly].keys())[-1]]
        # nod = monthrange(int(ly),int(lm))
    # def get_labels(self,order_dates):
    #     print("Recieved : ",order_dates)
    #     data = {}
    #     month_data = []
    #     data["year"]=cur[list(order_dates.keys())[0]]
    #     for k,v in order_dates[data["year"]].items():
    #         month_data[k]
    def get_month_data(self,month,year):
        cur = self.get_ordered_date()
        ly = list(cur.keys())[0]
        f=0
        year = str(year)
        # dates = []
        print(cur)
        # l=False
        # if(ly!=year):
        #     # l=True
        #     o = Old_Orders.objects.filter(email = self.email)
        #     for i in o:
        #         da=json.loads(i.data)
        #         k = list(da.keys())[0]
        #         if k==year:
        #             m = list(da[k].values())
        #             if str(month) in m:
        #                 f = 1
        #                 cur = da
        #                 break
        if (ly!=year):
            cur = { year : { str(month) : {  } } }            
        # l=False

        o = Old_Orders.objects.filter(email = self.email)
        for i in o:
            da=json.loads(i.data)
            k = list(da.keys())[0]
            if k==year:
                m = list(da[k].values())
                if str(month) in m:
                    for j,k in da[k][m].items():
                        if j in list(cur[year][str(month)].keys()):
                            for l,m in k.items():
                                cur[year][str(month)][j][l] = m
                        else:
                            cur[year][str(month)][j] = k
        
        cur_data = {}
        print(cur)
        try:
            cur_data = { year : { str(month) : cur[year][str(month)]  } }
        except:
            cur_data = { year : { str(month) : {  } } }
            # dates=[]
        # o = Overflown_Orders_Data.objects.filter(email = self.email)
        # for i in o:
        #     da=json.loads(i.overflown_data)
        #     k = list(da.keys())[0]
        #     if k==year:
        #         m = list(da[k].values())
        #         if str(month) in m:
        #             for j in list(da[k][m].values()):
        #                 cur_data[year][str(month)][j] = da[year][str(month)][j]
        
        print(cur_data)

        cur_data = cur_data[year][str(month)]
        # cur_data = dict(cur_data)
        # print(cur_data,type(cur_data))
        if len(cur_data)==0:
            return False
        data = {}
        data["dates"] = list(map(int,list(cur_data.keys())))
        # data["success"] = list(map(lambda x: [i['s'] for i in x] ,list(map(lambda x:list(x.values()),list(cur_data.values())))))
        # data["failed"] = list(map(lambda x: [i['f'] for i in x] ,list(map(lambda x:list(x.values()),list(cur_data.values())))))
        # data["success"] = list(map(lambda x:x["success"],list(cur_data.values())
        # data["failed"] = list(map(lambda x:x["failed"],list(cur_data.values())
        data["success"] = []
        data["order_data"] = cur_data
        print(data["dates"])
        data["failed"] = []
        data["dates"].sort(reverse=True)
        
        for i in data["dates"]:
            d = cur_data[str(i)]
            if len(d)>1:
                # data["success"].append([])
                # data["failed"].append([])
                d = list(d.values())
                
                data["success"].append(d[-1]["s"])
                data["failed"].append(d[-1]["f"])
            else:
                d = list(d.values())
                
                data["success"].append(d[-1]["s"])
                data["failed"].append(d[-1]["f"])
                


        return data


    def get_starting_month(self):
        date = str(self.date_created)
        return int(date.split()[0].split("-")[1])
    def get_years(self):

        # cur = self.get_ordered_date()
        # ly = list(cur.keys())[0]
        # year = [int(ly)]
        # month =  list(map(int,list(cur[ly].keys())))

        # o = Old_Orders.objects.filter(email=self.email)
        # for i in o:
        #     cur = json.loads(i.data)
        #     ly = list(cur.keys())[0]
        #     year.append(int(ly))
        #     t = list(map(int,list(cur[ly].keys())))
        #     for j in t:
        #         month.append(j)
        # year = list(set(year))
        # month = list(set(month))
        # year.sort()
        # month.sort()
        # return {"years": year,"months":month}
    
        year = json.loads(self.years)
        year = list(map(int,year))
        # o = Old_Orders.objects.filter(email=self.email)
        # for i in o:
        #     cur = json.loads(i.years)
        #     year.append(int(cur[0]))
        year = list(set(year))
        year.sort(reverse=True)
        return {"years":year}
    
    def get_all_completion_details(self,month,year):
        from datetime import datetime
        days = {"0":"Monday","1":"Tuesday","2":"Wednesday","3":"Thursday","4":"Friday","5":"Saturday","6":"Sunday"}
        # ly = list(cur.keys())[0]
        # cur_data = cur[ly][str(month)]
        cur = self.get_ordered_date()
        ly = list(cur.keys())[0]
        f=0
        year = str(year)
        # dates = []
        if (ly!=year):
            cur = { year : { str(month) : {  } } }            
        # l=False

        o = Old_Orders.objects.filter(email = self.email)
        for i in o:
            da=json.loads(i.data)
            k = list(da.keys())[0]
            if k==year:
                m = list(da[k].values())
                if str(month) in m:
                    for j,k in da[k][m].items():
                        if j in list(cur[year][str(month)].keys()):
                            for l,m in k.items():
                                cur[year][str(month)][j][l] = m
                        else:
                            cur[year][str(month)][j] = k
        
        cur_data = {}
        try:
            cur_data = { year : { str(month) : cur[year][str(month)] } }
        except:
            cur_data = { year : { str(month) : {  } } }
            # dates=[]
        # o = Overflown_Orders_Data.objects.filter(email = self.email)
        # for i in o:
        #     da=json.loads(i.overflown_data)
        #     k = list(da.keys())[0]
        #     if k==year:
        #         m = list(da[k].values())
        #         if str(month) in m:
        #             for j in list(da[k][m].values()):
        #                 cur_data[year][str(month)][j] = da[year][str(month)][j]
        
        

        cur_data = cur_data[year][str(month)]
        if len(cur_data)==0:
            return False
        data = {}
        t = list(map(int,list(cur_data.keys())))
        # t_t = list(cur_data.keys())))
        # print(t)
        t.sort()
        # data["status"] = list(map(lambda x: [i['c'] for i in x] ,list(map(lambda x:list(x.values()),list(cur_data.values())))))
        data['weekdays'] = [ days[str(datetime(int(year),int(month),i).weekday())] for i in t]
        data["dates"] = [ year+"-"+str(month)+"-"+str(i) for i in t ]
        # data["total"] = list(map(lambda x: [i['t'] for i in x] ,list(map(lambda x:list(x.values()),list(cur_data.values())))))
        data["date_time"]=[]
        for pos,item in enumerate(t):
            d = dict(cur[year][str(month)][str(item)])
            # data["d"].append(data["dates"][pos])
            # dd =data["dates"][pos]
            # print(len(d))
            if len(d)>1:
                for i in d.keys():
                    # print(i)
                    data["date_time"].append(data["dates"][pos] + " " + str(i))
            else:
                data["date_time"].append(data["dates"][pos] + " " + str(list(d.keys())[0]))
                        
        data['dates'].sort()
        data["date_time"].sort()
        # month = str(month)
        data["status"] = []
        data["total"] = []
        for i in data["date_time"]:
            time = i.split()[1]
            d = i.split()[0].split("-")[-1]
            print("dt  ",data["date_time"],"   ",time,"  ",d)
            data["status"].append(cur_data[d][time]["c"])
            # data["total"].append(cur_data[d][time]["s"] + cur_data[d][time]["f"])
            data["total"].append(cur_data[d][time]["t"])
        # return super(Order_DashBoard,self).save(*args,**kwargs)
        return data
        # if order_dates==None:
            # order_dates=self.process_ordered_dates()
    def get_ordered_date(self):
        print(len(self.ordered_dates))
        return json.loads(self.ordered_dates)