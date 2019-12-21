from django.shortcuts import render
from django.http import HttpResponse
from user.models import User

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
    print(req.COOKIES['wasche'])
    print("wasche" in req.COOKIES)
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
                data['profile_image'] = pi.profile_image.url
            # data=["ddd"]
            except:
                print("no image")
                data['profile_image'] = ""
            # data = json.dumps(data)
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
    data=check_cookie(request)

    if data==None:
        return render(request,"temp_index.html",{"data":False})
    else:
        return render(request,"temp_index.html",{"data":data})
    
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
    if data==None:
        return render(request,"temp_service.html",{"data":False})
    else:
        return render(request,"temp_service.html",{"data":data})
    
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
