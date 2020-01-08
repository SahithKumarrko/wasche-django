from django.shortcuts import render,redirect
from application.views import check_cookie
# Create your views here.
from user.models import User
from dashboard.models import Old_Orders
from django.utils import timezone
from django.http import HttpResponse
import json

import json
def open_dashboard_page(request):
    data = check_cookie(request)
    print("dash",data)
    if data==None:
        return redirect("/u/")
    else:
        # try:
        data = json.loads(data)
        print(type(data))
        u = User.objects.get(email="s@g.com")
        # print("got and saving")
    # u.order_dashboard.process_ordered_dates({"shirts":3,"pants":4,"s":3,"c":4,"f":1,"t":3})
    # u.order_dashboard.save()
        mr = {"1": "January","2":"February","3":"March","4":"April","5":"May","6":"June","7":"July","8":"August","9":"September","10":"October","11":"November","12":"December"}
        year = u.order_dashboard.get_years()

        month = u.order_dashboard.get_starting_month()
        d = str(timezone.now())
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
        return render(request,"dash.html",{"data":json.dumps(data),"ud":json.dumps({"y":year,"m":month})})
    


def getdata(request):
    data = {"s":True}
    try:
        email = request.POST["email"]
        m = request.POST["month"]
        y = request.POST["year"]
        u = User.objects.get(email = email)
        d = {}
        d = u.order_dashboard.get_month_data(m,y)
        print(d)
        data["data"] = d
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({"s":False}))
    return HttpResponse(json.dumps(data))