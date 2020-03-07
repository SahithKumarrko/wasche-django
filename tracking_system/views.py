from django.shortcuts import render
from application.views import check_cookie
from django.http import HttpResponse
# Create your views here.
def render_track(request):
    data=check_cookie(request)
    if data==None:
        return render(request,"/u/")
    else:
        from tracking_system.models import Tracker
        from user.models import User
        from dashboard.models import Order_DashBoard
        import json
        d = json.loads(data)
        res = {}
        try:
            u = User.objects.get(email=d["e"])
            dash = Order_DashBoard.objects.get(email=u)
            if(dash.recent_date==""):
                res["status"] = ""
            else:

                t = Tracker.objects.get(track_id = u,date = dash.recent_date,time=dash.recent_time)
                tt= json.loads(t.completed_status)
                res["status"] = t.type_op
                res["odate"] = str(t.created_date.strftime("%Y-%m-%d %H:%M:%S %p"))
                res["date"] = str(t.completion_date.strftime("%Y-%m-%d %H:%M:%S %p"))
                res["data"] = tt
        except Exception as exp:
            print(exp)
            res["status"]=""
        return render(request,"trackOrder.html",{"data":data,"cdata":json.dumps(res)})
    