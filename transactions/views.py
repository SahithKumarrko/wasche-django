from django.shortcuts import render,redirect
# from django.http import render
from django.views.decorators.csrf import csrf_exempt
import hashlib
import hmac
from django.conf import settings
import base64
from datetime import datetime
from django.http import HttpResponse
import random
import requests
import json
from application.views import check_cookie
from datetime import timedelta
import string
from wasche.custom_settings import settings as cust_set
from transactions.models import Transaction
@csrf_exempt
def check_transaction(request):
    print(request.POST)
    try:
        postData = {
            "oid" : request.POST["orderId"],
        "oamount" : request.POST["orderAmount"],
        "rid" : request.POST["referenceId"],
        "status" : request.POST["txStatus"],
        "payment_mode" : request.POST["paymentMode"],
        "msg" : request.POST["txMsg"],
        "txtime" : request.POST["txTime"],
       "sk" : cust_set.secret_key
        }
        print(postData)

        req = requests.post("https://wasche-backend-api.herokuapp.com/get_confirmation_encryption.php", data=postData,json=postData)
        print("Got")
        print(req.text)
        if "success" in postData["status"].lower() and req.text == request.POST["signature"]:
            from application.models import Plans
            t = Transaction.objects.get(order_id=int(postData["oid"]))
            t.referenceId = postData["rid"]
            t.completed_status = True
            t.save()
            print("modified transaction")
            p = Plans.objects.get(user=t.customer_email)
            p.plan = t.plan
            p.eligibility = t.eligibility
            p.notified = True
            p.date_created = datetime.strptime(datetime.now(tz=cust_set.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
            p.end_date = p.date_created + timedelta(minutes=+44640)
            p.regular_count = 0
            p.other_count = 0
            p.current_order_id = postData["oid"]
            p.save()
            print(p.date_created,p.end_date)
            

            print("succeeded")
        else:
            print("noo")
            t = Transaction.objects.get(order_id=int(postData["oid"]))
            t.delete()
    except Exception as exp:
        print(exp)
    return redirect("/dashboard")

def createOrderId(em,plan,amount):
    t = Transaction(customer_email = em,customer_name=em.first_name+" "+em.last_name,customer_phone_number=em.phone_number,plan = plan,amount = amount,eligibility = json.dumps(cust_set.plan[plan]["details"]))
    t.save()
    print("saving")
    return str(t.order_id)
    

    # return "/".join(str(datetime.now(tz=cust_set.ist_info).strftime("%Y-%m-%d %H:%M:%S %p")).split(" "))
    # print(signatureData)
    # message = bytes(signatureData,encoding='utf-8')
    # #get secret key from your config
    # secret = bytes(cust_set.secret_key,encoding='utf-8')
    # return base64.b64encode(hmac.new(secret, message,digestmod=hashlib.sha256).digest())
def check_amount(amount,u,p):
    try:
        if int(amount) == cust_set.plan[p]["cost"]:
            return True
        else:
            return False
    except:
        return False
    return False
def create_random_note():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(random.randint(5,25)))
def start_transaction(request):
    e=""
    res = {}
    u=None
    try:
        # appId= request.user[]
        # orderId= request.
        # try:
        #     print("1")
        e = check_cookie(request)
        
        if e==None:
            res["status"] = False
            res["err"] = "You have logged out."
            res["log"] = True
            return render(request,"check-billing.html",{"data":res})
    
        # except:
        #     print(request.user)
        
        
    except:
        res["status"] = False
        res["err"] = "You have logged out."
        res["log"] = True
        return render(request,"check-billing.html",{"data":res})
    try:
        e = json.loads(e)
        e=e["e"]
        print(e)
        from user.models import User
        u = User.objects.get(email=str(e))
        print(u)
    except Exception as err:
        print(err)
        res["status"] = False
        res["err"] = "You have logged out."
        res["log"] = True
        return render(request,"check-billing.html",{"data":res})
    if(check_amount(request.POST["amount"],u,request.POST["plan"])):

        postData = {
            "aid" : cust_set.appId, 
            "oid" : createOrderId(u,request.POST["plan"],request.POST["amount"]), 
            "oa" : request.POST["amount"], 
            "oc" : request.POST["cur"], 
            "on" : create_random_note(), 
            "cn" : u.first_name+" "+u.last_name, 
            "sk":cust_set.secret_key,
            "ce" : u.email,
            "cp" : u.phone_number,
            "rurl":"http://localhost:8000/b/check_status/",
            "nurl":"http://localhost:8000/b/check_status/"
            
        }
        print(postData)
        # sortedKeys = sorted(postData.keys())
        # print(sortedKeys)
        # signatureData = ""
        # for k in sortedKeys:
        #     # print(k)
        #     signatureData += str(postData[k])
        
        # header = {"charset=utf-8"}
        # print(signatureData)
        # payload = {"aid":,"sk":"6729fa7a6f252cf7663f040f4cf937f2206be6e5"}
        req = requests.post("https://wasche-backend-api.herokuapp.com/get_encryption.php?aid="+postData["aid"] + "&oid=" + postData["oid"], data=postData,json=postData)
        # postData["sig"] = req.text()
        
        # print(req.request)
        print(req.text)
        # print(req.headers)
        postData["sig"] = req.text
        print(postData)
        # from cashfree_sdk.payouts.beneficiary import Beneficiary
        # bene_add = Beneficiary.add(, "ankur", "ankur@cashfree.com", "9999999999", "aakjakjakja")
        postData["status"] = True
        if(req.status_code==200):
            return render(request,"check-billing.html",{"data":postData})

    res["status"] = False
    res["err"] = "Error conneting to the payment gatway. Try later."
    res["log"] = False
    return render(request,"check-billing.html",{"data":res})
