from django.shortcuts import render,redirect
from application.views import check_cookie
# Create your views here.
from user.models import User
from dashboard.models import Old_Orders
# from django.utils import timezone
from django.http import HttpResponse
from wasche.custom_settings import settings
import json
from datetime import datetime


def open_dashboard_page(request):
    print(request.POST)
    data = check_cookie(request)
    print("dash",data)
    if data==None:
        return redirect("/u/")
    else:
        # try:
        from application.models import Plans
        data = json.loads(data)
        print(type(data))
        u = User.objects.get(email=data["e"])
        # print("got and saving")
    # u.order_dashboard.process_ordered_dates({"shirts":3,"pants":4,"s":3,"c":4,"f":1,"t":3})
    # u.order_dashboard.save()
        mr = {"1": "January","2":"February","3":"March","4":"April","5":"May","6":"June","7":"July","8":"August","9":"September","10":"October","11":"November","12":"December"}
        year = u.order_dashboard.get_years()

        month = u.order_dashboard.get_starting_month()
        d = str(datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p"))
        y = d.split()[0].split("-")[0]
        d = d.split()[0].split("-")[1]
        month = [ month, int(d) ]
        if(int(y)!=int(year["years"][0])):
            year["years"].insert(0,int(y))
            print("year added")
            year["years"].sort(reverse=True)
            u.order_dashboard.years = json.dumps(year["years"])
            u.order_dashboard.save()

        # for i in year:

    # years = json.loads(u.order_dashboard.years)
    # months = u.order_dashboard.get_months()
        # # data = u.order_dashboard.get_ordered_date()
    # orders_month = u.order_dashboard.get_month_data(months[0],years[0])
    # orders_completion = u.order_dashboard.get_all_completion_details(months[0],years[0])
        # if u.order_dashboard.overflown == True:
        #     res = Overflown_Orders_Data.objects.get(email=u)
        #     for item in res:
        # if orders_month==None:
            
        # orders = od.process_ordered_dates({"shirts":3,"pants":4})
        # od.ordered_dates = json.dumps(orders['orders'])
        # print("Od : ",od.ordered_dates)
        # od.save()
        # orders = od.get_ordered_date()

        # except Exception as e:
        #     print(e)
    # da = {"data":{"months":months,"years":years,"month_data":orders_month,"completion_data":orders_completion}}
    # print(da)
    # da = json.dumps(da)

        pdata = {"notify":False,"cavailable":False}
        try:
            
            p = Plans.objects.get(user=u)
            print(datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p"))
            diff = p.end_date - datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
            pdata["diff"] = str(diff)
            pdata["cavailable"] = True
            pdata["c"] = p.extra_amount
            if diff.days<0:
                pdata["over"] = True
                p.plan = "None"
                p.save()
            elif diff.days==0:
                pdata["over"] = True
                p.plan = "None"
                p.save()
            else:
                # if diff.hours>=12:
                #     pdata["diff"] = pdata["diff"] + " PM"
                # else:
                #     pdata["diff"] = pdata["diff"] + " AM"

                pdata["over"] = False
                
            if p.notified==True:
                pdata["notify"] = True
                p.notified = False
                p.save()
            print("over")
        except:
            pdata["over"] = True
        if pdata["over"]==True:
            pdata["plans"] = []
            from wasche.custom_settings import settings as sett
            for i in sett.plan.keys():
                pdata["plans"].append((i,sett.plan[i]))
        print(pdata)
        rtc = 0
        if u.plans.plan!="None":
            rtc = settings.regular_count[u.plans.plan]
        return render(request,"dash.html",{"data":json.dumps(data),"ud":json.dumps({"y":year,"m":month}),"pdata":pdata,"rcount":u.plans.regular_count,"ocount":u.plans.other_count,"rtcount":rtc,"otcount":settings.other_count})
    


def getdata(request):
    data = {"s":True}
    try:
        email = request.POST["email"]
        m = request.POST["month"]
        y = request.POST["year"]
        u = User.objects.get(email = email)
        d = {}
        d = u.order_dashboard.get_month_data(m,y)
        try:
            if "order_data" in d:
                xx = d["order_data"]
                for i in xx.keys():

                    x = xx[i]
                    x = {k: v for k, v in sorted(x.items(), key=lambda item: item[0],reverse=True)}
                    print("\n\nNew : \n\n",x)
                    d["order_data"][i] = x
        except:
            print("error")
               
        data["data"] = d
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({"s":False}))
    return HttpResponse(json.dumps(data))

from django.views.decorators.csrf import csrf_exempt
import requests
from user.models import Notifications

def onsignal(msg,u):
    from user.models import OneSignal
    ons = OneSignal.objects.filter(email = u)
    pid = []
    for i in ons:
        pid.append(i.pid)
    
    header = {"Content-Type": "application/json; charset=utf-8"}

    payload = {"app_id": "df0790ca-561e-44c3-8cb2-9d1b78bf0bab",
            "include_player_ids": pid,
            "contents": {"en": msg},"headings":{"en":"Wasche"},"data":{"got":"soomething"},"url":"localhost:8000"}
    
    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
    
    print(req.status_code, req.reason)
    print(req)
    return "Complete"

@csrf_exempt
def update_data(request):
    print(request.POST)
    ddd = json.loads(request.POST["user"])
    print(ddd)
    data = ddd["data"]
    user = ddd["cred"]
    u = User.objects.get(email=user["email"])
    from tracking_system.models import Tracker
    try:
        rrr = u.order_dashboard.update_dashboard(ddd["date"],ddd["time"],data)
        print("Updated Dashboard   ",rrr)
        u.save()
        t = Tracker.objects.filter(track_id = u,date = ddd["date"],time=ddd["time"])
        dat = {}
        dat["data"] = data
        dat["type"] = ddd["type"]
        print(len(t))
        for ii in t:
            ii.update_operation(dat)
            ii.save()
        noti = Notifications(type_msg = "tracking",email = u,sent_from = "Admin",title = ddd["title"],msg=ddd["msg"],seen=False)
        noti.save()
        # onsignal("Your order has been recieved at our warehouse. You can track the order details in tracking page.",u)
        onsignal(ddd["msg"],u)
        return HttpResponse("Success")
    except Exception as exp:
        print(exp)
        
        # dd = u.order_dashboard.update_dashboard(request.POST["date"],request.POST["time"],data)
        # noti = Notifications(type_msg = "tracking",email = u,sent_from = "Admin",title = "Completed Processing Your Order",msg="Your order has been processed. You can track the order details in tracking page.",seen=False)
        # noti.save()
        # onsignal("Your order has been completed processing. You can track the order details in tracking page.",u)
        
        # return "Success"
    return HttpResponse("Error")

@csrf_exempt
def update_data_new(request):
    print(request.POST)
    ddd = json.loads(request.POST["user"])
    print(ddd)
    data = ddd["data"]
    user = ddd["cred"]
    u = User.objects.get(email=user["email"])
    from tracking_system.models import Tracker
    try:
        dd = u.order_dashboard.process_ordered_dates(data)
        print(dd)
        # t = Tracker(track_id = u,date = dd["date"],time=dd["time"])
        # dat = data
        # dat["type"] = request.POST["type"]
        # t.update_operation(dat)
        # t.save()
        noti = Notifications(type_msg = "tracking",email = u,sent_from = "Admin",title = "Recieve of order",msg="Your order has been recieved at our warehouse. You can track the order details in tracking page.",seen=False)
        noti.save()
        # onsignal("Your order has been recieved at our warehouse. You can track the order details in tracking page.",u)
        onsignal("Your order has been recieved at our warehouse. You can track the order details in tracking page.",u)
        return HttpResponse(json.dumps(dd))
    except Exception as exp:
        print(exp)
        
        # dd = u.order_dashboard.update_dashboard(request.POST["date"],request.POST["time"],data)
        # noti = Notifications(type_msg = "tracking",email = u,sent_from = "Admin",title = "Completed Processing Your Order",msg="Your order has been processed. You can track the order details in tracking page.",seen=False)
        # noti.save()
        # onsignal("Your order has been completed processing. You can track the order details in tracking page.",u)
        
        # return "Success"
    return HttpResponse("Error")
