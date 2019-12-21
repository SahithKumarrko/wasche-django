from django.shortcuts import render,redirect
from application.views import check_cookie
# Create your views here.
def open_dashboard_page(request):
    data = check_cookie(request)
    print("dash",data)
    if data==None:
        return redirect("/u/")
    else:
        return render(request,"dash.html",{"data":data})