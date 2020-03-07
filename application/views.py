from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from user.models import User,OneSignal,Notifications

def send_mail_to_client(email,subject,text_msg,html_message):
    # from smtplib import SMTPException
    
    from django.core.mail import EmailMultiAlternatives
    try:
        msg = EmailMultiAlternatives(subject,text_msg,"wasche.services@gmail.com",[email])
        msg.attach_alternative(html_message, "text/html")
        msg.send()
        print("sent")
    except Exception as e:
        print("Error Sending Mail",e)
        raise e
def check_cookie(req):
    print("entered")
    # print(req.COOKIES['wasche'])
    # print("wasche" in req.COOKIES)
    data=[]
    try:
        if "wasche" in req.COOKIES:
            print("yes")
            data=req.COOKIES['wasche']
            import json
            data=data.replace("'","\"")
            data=json.loads(data)
            
            pi = User.objects.get(email=data['e'])
            try:
                data['profile_image'] = ""
                if pi.profile_image!="No":
                    data['profile_image'] = pi.profile_image
            # data=["ddd"]
            except:
                print("no image")
                data['profile_image'] = ""
            # data = json.dumps(data)
            try:
                data["pid"] = []
                o = OneSignal.objects.filter(email = pi)
                print(o)
                for i in o:
                    if i.enabled:
                        data['pid'].append(i.type)
            except:
                print("no data")
            print(data)
            return json.dumps(data)
    except Exception as e:
        print(e)
        return None
    return None

def home(request):
    # if User.objects.filter(email="t@gmail.com").exists():
    #     print("yes")
    #     User.objects.filter(email="t@gmail.com").delete()
    # co = Contracts(contract_name="No College",contract_address="",contract_phone_number="",contract_zip_code="",contract_country="",contract_state="")
    # co.save()
    # try:
    #     print("GET")
    #     r = request.GET
    #     for i in r:
    #         print(i)
    #     print("Post")
        
    #     r = request.POST
    #     for i in r:
    #         print(i)
    #     print(len(request.GET))
    #     print(request.POST["data"])
    #     # print("requestGET : ",request.GET["got"])
    #     # print("request POST : ",request.POST["got"])
    # except Exception as e:
    #     print("nothing : ",e)
    # print(request)
    # print("GET\n",request.GET,"\n","POST\n",request.POST)
    data=check_cookie(request)
    pdata= {"plans":[]}
    from wasche.custom_settings import settings as sett
    for i in sett.plan.keys():
        pdata["plans"].append((i,sett.plan[i]))
    # print(pdata)
    if data==None:
        return render(request,"temp_index.html",{"data":False,"pdata":pdata})
    else:
        return render(request,"temp_index.html",{"data":data,"pdata":pdata})
    
    # return render(request,"temp_index.html")

def about(request):
    data=check_cookie(request)
    if data==None:
        return render(request,"temp_about.html",{"data":False})
    else:
        return render(request,"temp_about.html",{"data":data})
    
    # return render(request,"temp_about.html")

def services(request):
    data=check_cookie(request)
    pdata= {"plans":[]}
    from wasche.custom_settings import settings as sett
    for i in sett.plan.keys():
        pdata["plans"].append((i,sett.plan[i]))
    # print(pdata)
    if data==None:
        return render(request,"temp_service.html",{"data":False,"pdata":pdata})
    else:
        return render(request,"temp_service.html",{"data":data,"pdata":pdata})
    
    # return render(request,"temp_service.html")

def contact(request):
    data=check_cookie(request)
    if data==None:
        return render(request,"contact.html",{"data":False})
    else:
        return render(request,"contact.html",{"data":data})
    
    # return render(request,"contact.html")

def subscribe(request):
    from user.models import User
    # from user.views import send_mail_to_client
    from application.models import Subscribers
    try:
        email = request.POST['widget-subscribe-form-email']
        from django.core.exceptions import ValidationError

        from django.core.validators import validate_email
        try:
            validate_email(email)
        except ValidationError:
            return HttpResponse("")
        try:
            u = User.objects.get(email=email)
            u.news_letter_subscription = "on"
            u.save()
            
        except:
            print("Not found")
            try:
                if not Subscribers.objects.filter(email=email).exists():
                    print("no")
                    su = Subscribers(email=email)
                    su.save()
            except Exception as e:
                print(e)
                print("error")
                return HttpResponse("Error")
        msg="<style>@import url('https://fonts.googleapis.com/css?family=Open+Sans&display=swap');</style>"     
        msg=msg+"<div style=\"font-family:'Open Sans',Arial,sans-serif;\"><div style='min-height:4rem;width:100%;display:block;border-bottom:1px solid #c5c5c5;margin-bottom:10px;'><div style='width:fit-content;height:fit-content;margin:auto;display:flex;justify-content:center;align-content:center;'><a href='https://wasche-services.herokuapp.com' style='color:black;font-size:1.6rem;text-decoration:none;text-transform:uppercase;letter-spacing:2px;font-weight:bold;padding:0;margin:0;text-shadow:1px 1px 1px rgba(0,0,0,0.1);'>Wasche</a></div></div>"
        msg=msg+"<h2 style='margin-bottom:5px;padding:5px;margin-top:10px;'>Thank you for subscribing to our news letter.</h2><h4> We are happy to see you here. You will recieve all the latest updates including amazing vouchers and discounts.</h4><br><br><p style='font-size:15px'>Than you, <b>Wasche Laundry Services.</b></p></div> "
    
        send_mail_to_client(email,"Subscription Letter","Thank you for subscribing to our news letter.\n\n We are happy to see you here. You will recieve all the latest updates including amazing vouchers and discounts.\n\nThank you, \nWasche Laundry Services.",msg)
        
        
    except:
        return HttpResponse("Error")
    return HttpResponse("success")

def contact_mail(request):
    from user.models import User
    # from user.views import send_mail_to_client
    from application.models import Contact
    import json
    data = {"c":True,"sent":False,"ef":False}
    try:
        name= request.POST["name"]
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        from django.core.exceptions import ValidationError

        from django.core.validators import validate_email
        try:
            validate_email(email)
        except ValidationError:
            data['ef']=True
            return HttpResponse(json.dumps(data))
        try:
            cu = Contact(name=name,email=email,subject=subject,message=message)
            cu.save()
            data['sent']=True
        except Exception as e:
            print(e)
            print("error")
            data['c']=False
            return HttpResponse(json.dumps(data))            
            
        msg="<style>@import url('https://fonts.googleapis.com/css?family=Open+Sans&display=swap');</style>"     
        msg=msg+"<div style=\"font-family:'Open Sans',Arial,sans-serif;\"><div style='min-height:4rem;width:100%;display:block;border-bottom:1px solid #c5c5c5;margin-bottom:10px;'><div style='width:fit-content;height:fit-content;margin:auto;display:flex;justify-content:center;align-content:center;'><a href='https://wasche-services.herokuapp.com' style='color:black;font-size:1.6rem;text-decoration:none;text-transform:uppercase;letter-spacing:2px;font-weight:bold;padding:0;margin:0;text-shadow:1px 1px 1px rgba(0,0,0,0.1);'>Wasche</a></div></div>"
        msg=msg+"<h2 style='margin-bottom:5px;padding:5px;margin-top:10px;'>Thank you for contacting us.</h2><h4> Your information has been sent to our professional workers.<br>You will soon here from us regarding your enquiry.</h4><br><br><p style='font-size:15px'>Than you, <b>Wasche Laundry Services.</b></p></div> "
    
        send_mail_to_client(email,"Contact Information","Thank you for contacting us.\n\nYour information has been sent to our professional workers.\nYou will soon here from us regarding your enquiry.\n\nThank you, \nWasche Laundry Services.",msg)
        
        
    except:
        data['sent']=False
    return HttpResponse(json.dumps(data))

def onsignal(request):
    import requests
    import json

    header = {"Content-Type": "application/json; charset=utf-8"}

    payload = {"app_id": "df0790ca-561e-44c3-8cb2-9d1b78bf0bab",
            "include_player_ids": ["3cd0f7d8-08a5-4b95-ad85-5d4d60338da1"],
            "contents": {"en": "working"},"headings":{"en":"Wasche"},"data":{"got":"soomething"},"url":"localhost:8000"}
    
    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
    
    print(req.status_code, req.reason)
    print(req)
    return HttpResponse("okk")
    # api = ""
    # try:
    #     api = request.POST["appId"]
    # except:
    #     api = request.GET["appId"]
    # print(api)
    # return HttpResponse("OneSignalWorker")

def logout(request):
    print("logging out")
    response = HttpResponseRedirect("/u/")
    response.delete_cookie("wasche")
    return response

def update_notification_setting(request):
    import json
    data = check_cookie(request)
    res = {"s":True,"sd":False}
    if data==None:
        res["s"]=False
        res["sd"]=True
    else:
        data = json.loads(data)
        print(data,type(data))
        u=None
        i=""
        no=None
        try:
            if request.POST["type"]=="0":
                try:
                    i = request.POST["pid"]
                except:
                    res["nf"] = True
                    res["s"]=False
                    return HttpResponse(json.dumps(res))
                try:
                    u = User.objects.get(email=data["e"])
                except:
                    res["ne"] = True
                    res["s"]=False
                    return HttpResponse(json.dumps(res))
                try:
                    o = OneSignal.objects.get(email=u,pid=i)
                except:
                    res["no"] = True
                    res["s"]=False
                    return HttpResponse(json.dumps(res))
                try:
                    o.enabled = False if o.enabled else True
                    o.save()
                except:
                    res["f"] = True
                    res["s"]=False
                    return HttpResponse(json.dumps(res))
            if request.POST["type"]=="2":
                try:
                    u = User.objects.get(email=data["e"])
                except:
                    res["ne"] = True
                    res["s"]=False
                    return HttpResponse(json.dumps(res))
                try:
                    o = OneSignal.objects.filter(email=u,pid=request.POST["pid"])
                    if len(o)==0:
                        o = OneSignal(email=u,pid=request.POST["pid"],type_os=request.POST["agent-type"])
                        o.save()
                    else:
                        fou = False
                        for i in o:
                            if i.type == request.POST["agent-type"]:
                                i.enabled = True
                                fou = True
                                i.save()
                                
                        if fou==False:
                            o = OneSignal(email=u,pid=request.POST["pid"],type=request.POST["agent-type"])
                            o.save()
                            
                except Exception as e:
                    print(e)
                    res["f"] = True
                    res["s"]=False
                    return HttpResponse(json.dumps(res))
            if request.POST["type"]=="3":
                try:
                    i = request.POST["pid"]
                except:
                    res["nf"] = True
                    res["s"]=False
                    return HttpResponse(json.dumps(res))
                try:
                    u = User.objects.get(email=data["e"])
                except:
                    res["ne"] = True
                    res["s"]=False
                    return HttpResponse(json.dumps(res))
                try:
                    o = OneSignal.objects.get(email=u,pid=i)
                except:
                    res["no"] = True
                    res["s"]=False
                    return HttpResponse(json.dumps(res))
                try:
                    o.enabled = False
                    o.save()
                except:
                    res["f"] = True
                    res["s"]=False
                    return HttpResponse(json.dumps(res))

    
            
        except:
            res["s"]=False
            res["sp"]=False
        return HttpResponse(json.dumps(res))

def offline(request):
    return render(request,"offline.html")

def get_notifications(request):
    import json
    data = check_cookie(request)
    
    res = {"s":True}
    if(data==None):
        res["s"] = False
        return HttpResponse(json.dumps(res))
    else:
        data = json.loads(data)
        e = data["e"]
        u=None
        noti = None
        try:
            u = User.objects.get(email=e)
        except:
            res["s"] = False
            res["e"] = True
            return HttpResponse(json.dumps(res))
        try:
            # n = int(request.POST["n"])
            n=10
            f = int(request.POST["f"])
            c = 1
            res["data"] = []
            noti = Notifications.objects.filter(email=u).order_by("-date_created")
            print(noti)
            for i in noti:
                print(i.date_created)
                if (c>=f and c<=n):
                    print("addding")
                    res["data"].append({"id":i.id,"type":i.type_msg,"from":i.sent_from,"title":i.title,"msg":i.msg,"date":str(i.date_created.strftime("%Y-%m-%d %H:%M:%S %p")),"seen":i.seen,"img_url":i.image_url})
                else:
                    break
                c = c+1
            return HttpResponse(json.dumps(res))
        except Exception as exp:
            print(exp)
            res["s"] = False
            res["err"] = True
    return HttpResponse(json.dumps(res))


def get_new_notifications(request):
    import json
    data = check_cookie(request)
    data = json.loads(data)
    res = {"s":True}
    if(data==None):
        res["s"] = False
        return HttpResponse(json.dumps(res))
    else:
        e = data["e"]
        u=None
        noti = None
        try:
            u = User.objects.get(email=e)
        except:
            res["s"] = False
            res["e"] = True
            return HttpResponse(json.dumps(res))
        try:
            d = request.POST["date"]
            res["data"] = []
            c=0
            noti = Notifications.objects.filter(email=u).order_by("-date_created")
            for i,j in enumerate(noti):
                k = str(j.date_created.strftime("%Y-%m-%d %H:%M:%S %p"))
                print(d)
                if k != d and c==i:
                    res["data"].append({"id":i.id,"type":i.type_msg,"from":j.sent_from,"title":j.title,"msg":j.msg,"date":str(j.date_created.strftime("%Y-%m-%d %H:%M:%S %p")),"seen":j.seen,"img_url":j.image_url})
                else:
                    break
            return HttpResponse(json.dumps(res))
        except Exception as e:
            print(e)
            res["s"] = False
            res["err"] = True
    return HttpResponse(json.dumps(res))


def update_notifications(request):
    import json
    data = check_cookie(request)
    data = json.loads(data)
    res = {"s":True}
    if(data==None):
        res["s"] = False
        return HttpResponse(json.dumps(res))
    else:
        e = request.POST["id"]
        noti = None
        try:
            noti = Notifications.objects.filter(id=int(e))
            if len(noti)==1:
                for i in noti:
                    if i.seen==False:
                        i.seen=True
                        i.save()
            elif len(noti)>1:
                res["mn"]=True
                res["s"]=False
            else:
                res["nf"]=True
                res["s"]=False
                    
        except Exception as e:
            print(e)
            res["s"] = False
            res["err"] = True
    return HttpResponse(json.dumps(res))


from user.models import Notifications
from dashboard.views import onsignal
from delivery_executives.models import Deliver_Executive,ongoing_delivery
from django.views.decorators.csrf import csrf_exempt
import threading
import json

def thread_task(data):
    print(data)
    # data = data[0]
    try:
        for i in data["u"]:
            if i.plans.plan != "None":
                noti = Notifications(type_msg = "notify",email = i,sent_from = "Admin",title = data["title"],msg=data["msg"],seen=False)
                noti.save()
                onsignal(data["msg"],i)
        return HttpResponse("Success")
    except Exception as exp:
        print(exp)


@csrf_exempt
def notify_user(request):
    print(request.POST)
    ddd = json.loads(request.POST["data"])
    data = ddd
    print(ddd)
    try:
        de = Deliver_Executive.objects.get(id=int(data["id"]),name = data["name"])
        cn = de.contract_name
        print(cn)
        u = User.objects.filter(contract_name = cn)
        print(u)
        if data["type"] == "initial":
            o = ongoing_delivery(name = de,on_going = "initialized")
            o.save()
        if data["type"] == "finish":
            o = ongoing_delivery.objects.get(name = de)
            o.on_going = "delivering"
            o.save()
        
        data["u"] = u
        t = threading.Thread(target=thread_task,args=[data])
        t.setDaemon(True)
        t.start()
    except Exception as exp:
        print(exp)
        return HttpResponse("Error")
    return HttpResponse("Success")



