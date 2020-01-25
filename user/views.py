from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .models import User
from django.contrib import auth
# from django.utils import timezone
from wasche.custom_settings import settings
from django.middleware import csrf
from django.template import RequestContext
from application.views import send_mail_to_client
from django.shortcuts import redirect
from datetime import datetime
# Create your views here.
# from datetime import datetime
from django.db.models.signals import pre_delete
from application.views import check_cookie
from .models import Password_Reset
# from user.signals import post_delete_user
# pre_delete(post_delete_user,sender=User)
import functools
import gzip
import re
from difflib import SequenceMatcher
from pathlib import Path
import pyqrcode
from wasche.custom_settings import settings
# from django.conf import settings
from django.core.exceptions import (
    FieldDoesNotExist, ImproperlyConfigured, ValidationError,
)
from django.utils.functional import lazy
from django.utils.html import format_html, format_html_join
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _, ngettext


@functools.lru_cache(maxsize=None)
def get_default_password_validators():
    return get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)


def get_password_validators(validator_config):
    validators = []
    for validator in validator_config:
        try:
            klass = import_string(validator['NAME'])
        except ImportError:
            msg = "The module in NAME could not be imported: %s. Check your AUTH_PASSWORD_VALIDATORS setting."
            raise ImproperlyConfigured(msg % validator['NAME'])
        validators.append(klass(**validator.get('OPTIONS', {})))

    return validators



def validate_password(password, user=None, password_validators=None):
    """
    Validate whether the password meets all validator requirements.

    If the password is valid, return ``None``.
    If the password is invalid, raise ValidationError with all error messages.
    """
    errors = []
    help_texts = []
    if password_validators is None:
        password_validators = get_default_password_validators()
    for validator in password_validators:
        try:
            validator.validate(password, user)
        except ValidationError as error:
            help_texts.append(validator.get_help_text())
            errors.append(error)
    return help_texts




def password_validators_help_texts(password_validators=None):
    """
    Return a list of all help texts of all configured validators.
    """
    help_texts = []
    if password_validators is None:
        password_validators = get_default_password_validators()
    for validator in password_validators:
        help_texts.append(validator.get_help_text())
    return help_texts



def _password_validators_help_text_html(password_validators=None,password=""):
    """
    Return an HTML string with all help texts of all configured validators
    in an <ul>.
    """
    help_texts = validate_password(password)
    print(help_texts)
    help_items = format_html_join('', '<li>{}</li>', ((help_text,) for help_text in help_texts))
    return format_html('<ul>{}</ul>', help_items) if help_items else ''



def user_login_page(request):
    data=check_cookie(request)
    if data==None:
        return render(request,"user.html",{"data":False})
    else:
        return redirect("/dashboard")



def profile(request):
    from application.models import Plans
    data=check_cookie(request)
    if data==None:
        return redirect("/u/")
    else:
        import json
        # from contracts.models import Contracts
        dd= json.loads(data)
        u = User.objects.get(email=dd["e"])
        ud = {}
        ud["email"] = u.email
        ud["fn"] = u.first_name
        ud["ln"] = u.last_name
        ud["pav"] = True
        ud["pp"] = u.profile_image
        if ud["pp"]=="No":
            ud["pav"] = False

        ud["fullname"] = u.first_name + " " + u.last_name
        ud["addr"] = u.address
        # c = Contracts.objects.get(contract_name=u.contract_name)
        ud["col"] = u.contract_name.contract_name
        ud["coladdr"] = u.contract_name.contract_address
        p = Plans.objects.get(user = u)
        if p.plan=="None":
            ud["plan"] = "Currently you have no plan."
        else:
            ud["plan"] = p.plan + " Kit."
        print(ud)
        ud["tot"] = u.order_dashboard.total_orders
        qr = u.qr_code_data
        return render(request,"profile.html",{"data":data,"ud":ud,"qr_code":qr.decode('utf-8')})



def login(request):
    email = request.POST["clientEmail"]
    password = request.POST["clientPassword"]


    # uu=User.objects.get(email=email)
    # uu.set_password("1234rko")
    # uu.save()
    # if(len(validate_password(password=password))==0):
    #     User.objects._create_user(email="tt@gmail.com",password=password,first_name="sahith",last_name = "kumar",address="adsd",phone_number="sdasd",zip_code="sadsad",contracts="sadsad",contracts_address="sdsad",gender="sadas")
        
    #     d="done"
    # else:
    #     d="ee"
    # data = {
    #     'log' : User.objects.filter(email=email,password=password).exists()
    # }
   
    import json
    data = {"c":True,"g":False,"ee":False}
    
    try:
        from django.core.exceptions import ValidationError

        from django.core.validators import validate_email
        try:
            validate_email(email)
            # print("pass e")
            print("received ",email)
            u =User.objects.get(email = email)
            print("complete")
            
            if u.check_password(password):
                    # lo=u.first_name+"   "+u.email
                print("enter")
                u.last_login=datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
                u.save()
                pr = Password_Reset.objects.filter(email=u)
                if pr:
                    pr.delete()

                # response.delete_cookie("vote")
                # max_age = 24*60*365 # two weeks
                # expires = datetime.strftime(datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
                    
                data['g']=True
                response=HttpResponse(json.dumps(data))
                response.set_cookie('wasche', {"e":u.email,"fn":u.first_name,"ln":u.last_name,"gender":u.gender},6307200)
            
                return response
            else:
                data['ip']=False
        except ValidationError:
            data['ee']=True
        except:
            data['ie']=True
    except:
        data['c']=False
    response=HttpResponse(json.dumps(data))

    return response
def register(request):

    # uu=User.objects.get(email=email)
    # uu.set_password("1234rko")
    # uu.save()
    # if(len(validate_password(password=password))==0):
    #     User.objects._create_user(email="tt@gmail.com",password=password,first_name="sahith",last_name = "kumar",address="adsd",phone_number="sdasd",zip_code="sadsad",contracts="sadsad",contracts_address="sdsad",gender="sadas")
        
    #     d="done"
    # else:
    #     d="ee"
    # data = {
    #     'log' : User.objects.filter(email=email,password=password).exists()
    # }
    from contracts.models import Contracts
   
    import json
    data = {"c":True,"g":False,"ee":False,"inve":False}
    
    try:
        
        email = request.POST["email"]
        password = request.POST["pswd"]

        from django.core.exceptions import ValidationError

        from django.core.validators import validate_email
        try:
            validate_email(email)
            # print("pass e")
            u = User.objects.get(email = email)
            data['inve']=True
            
        except ValidationError:
            data['ee']=True
        except:
            try:
                fn=request.POST["first_name"]
                ln=request.POST["last_name"]
                phno=request.POST["phno"]
                addr=request.POST["address"]
                gender=request.POST["gender"]
                col=request.POST["college"]
                con_u = Contracts.objects.get(contract_name = col)
                coladd=request.POST['coladdress']
                
                u=User.objects._create_user(email=email,password=password,first_name=fn,last_name=ln,gender=gender,address=addr,phone_number=phno,zip_code="500076",contract_name=con_u ,last_login=datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p"))
                print("User created")
                u = User.objects.get(email=email)
                print("got user and changing")
                qr = pyqrcode.create(json.dumps({"email":u.email,"first_name":u.first_name,"last_name":u.last_name,"gender":u.gender,"contract_name":u.contract_name.contract_name,"contract_address":u.contract_name.contract_address}))
                dta = "data:image/png;base64," + qr.png_as_base64_str()
                u.qr_code_data = bytes(dta,'utf-8')
                u.save()
                from user.models import Notifications
                noti = Notifications(type_msg = "notify",email = u,sent_from = "Wasche",title = "Welcome!",msg = "Welcome "+u.first_name + ". We are happy to see you here. We hope you like our service. If you have any issues please send us a contact mail we will verify your response. Thank you.",seen = False)
                noti.save()
                # u.last_login=datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
                # u.save()
            # response.delete_cookie("vote")
            # max_age = 24*60*365 # two weeks
            # expires = datetime.strftime(datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
                
                data['g']=True
                response=HttpResponse(json.dumps(data))

                response.set_cookie('wasche', {"e":email,"fn":fn,"ln":ln,"gender":gender},6307200)
                return response
            except Exception as exp:
                print("Reg Error  ",exp)

                data['c']=False
        
            
                
    except:
        data['c']=False
    response=HttpResponse(json.dumps(data))

    return response
# print(validate_password("191023"))

def check_user(request):
    email = request.POST["email"]

    import json
    data = {"c":True,"g":False,"ee":False,"inve":False}
    
    try:
        from django.core.exceptions import ValidationError

        from django.core.validators import validate_email
        try:
            validate_email(email)
            u=User.objects.get(email=email)
            data['inve']=True
        except ValidationError:

            data['ee']=True
        except:
            print("sss")

            data['g']=True
            response=HttpResponse(json.dumps(data))
            return response
                
    except:
        data['c']=False
    response=HttpResponse(json.dumps(data))

    return response



def contracts(request):
    from contracts.models import Contracts
    import json
    data = {"c":True,"s":True}
    
    try:
        try:
            res={'name':[],'address':[]}
            d=Contracts.objects.values('contract_name','contract_address')
            d=list(d)
            for item in d:
                res['name'].append(item['contract_name'])
                res['address'].append(item['contract_address'])
            # print(d.contracts_name)
            data['res']=res
        except:
            print("sss")

            data['s']=False
                
    except:
        data['c']=False
    response=HttpResponse(json.dumps(data))

    return response
 


def check_resend_password(request):
    # email = decrypt(request.POST["slug"])
    
    # print(email)
    import json
    data = {"c":True,"g":False,"e":False}
    
    try:
        uid = request.POST["slug"]
        # from django.core.exceptions import ValidationError
        # from django.core.validators import validate_email
        try:
            # validate_email(email)

           
            pr = Password_Reset.objects.filter(uuid_id = uid)
            if pr:
                print("present")

                for i in pr:
                    print(i.email)
                    up = User.objects.get(email=i.email)
                    data['e'] = up.first_name +" " + up.last_name
                    print(up.first_name +" " + up.last_name,data['e'])

                    dif =  str(datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p") - i.date_sent)
                    print(dif)
                    dif = dif.split(":")
                    if not (int(dif[0]) >= 1 and int(dif[0])>0):
                        print("still there")
                        data['g']=True
                    else:
                        pr.delete()
                data['s']=True
            
        except:
            data['g']=False
    except:
        data['c']=False
    response=HttpResponse(json.dumps(data))

    return response


def confirm_reset_pswd(request):
    import json
    data = {"c":True,"g":False,"e":False}
    
    try:
        email = request.POST["slug"]

        from django.core.exceptions import ValidationError
        from django.core.validators import validate_email
        try:
            pr = Password_Reset.objects.filter(uuid_id = email)
            if pr:
                print("present")

                for i in pr:
                    print(i)
                    print(i.email)
                    dif =  str(datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p") - i.date_sent)
                    dif = dif.split(":")
                    if not (int(dif[0]) >= 1 and int(dif[0])>0):
                        print("still there")
                        data['g']=True
                        em = str(i.email)
                        print(em)
                        # up = User
                        up = User.objects.get(email=em)
                        
                        up.set_password(request.POST['clientPassword'])
                        up.save()
                pr.delete()
                data['s']=True
            
        except:
            data['g']=False
    except:
        data['c']=False
    response=HttpResponse(json.dumps(data))

    return response


def reset_pswd_page(request,slug):
    # aaa=encrypt("tt@gmail.com")
    # print(aaa)
    # print(decrypt(aaa))
    return render(request,"reset.html",{"slug":slug})
import uuid


def set_reset_pswd(request):
    email = request.POST['clientEmail']
    print(email)
    d_s = datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
    import json
    data = {"c":True,"g":True,"s":False,"ef":False,"inem":False}
    
    try:
        from django.core.exceptions import ValidationError
        from smtplib import SMTPException
        from django.core.validators import validate_email
        try:
            
            validate_email(email)

            up = User.objects.get(email=email)
            print("found")
            pr = Password_Reset.objects.filter(email = up)
            if pr:
                print("present")
                pr.delete()
                print("completed")
            encoded_text = str(uuid.uuid1()).lower()
            btn="<div style='display:block;width:fit-content;margin-top:20px;'><a href='#' onclick='console.log(\"Sdsad\");' style='cursor:pointer;padding:10px;text-transform:uppercase;font-size:14px;color:white;background:#019875;outline:none;border-radius:5px;border:1px solid #019875;text-decoration:none;'><span>Reset Password</sapn></a></p></div>"
            msg="<style>@import url('https://fonts.googleapis.com/css?family=Open+Sans&display=swap');</style>"       
            msg=msg+"<div style=\"font-family:'Open Sans',Arial,sans-serif;\"><div style='min-height:4rem;width:100%;display:block;border-bottom:1px solid #c5c5c5;margin-bottom:10px;'><div style='width:fit-content;height:fit-content;margin:auto;display:flex;justify-content:center;align-content:center;'><a href='https://wasche-services.herokuapp.com' style='color:black;font-size:1.6rem;text-decoration:none;text-transform:uppercase;letter-spacing:2px;font-weight:bold;padding:0;margin:0;text-shadow:1px 1px 1px rgba(0,0,0,0.1);'>Wasche</a></div></div>"
            # msg=msg+"<h3 style='margin-bottom:5px;padding:5px;'>Thank you for subscribing to your website.</h3><h5> We are happy to see you here. You will recieve all the latest updates including amazing vouchers and discounts.</h5></div> ";                      // Set email format to HTML
            msg=msg+"<div style='width:fit-content;margin:auto;'><p style='font-size:14px;'><b><span style='font-size:18px'>Hello,</span></b><br><br>We recieved a request to reset your password.<br><br>Click on the below link in order to reset your password.<br><b>Note : </b>This link will expire in another 60 minutes.<br><br><div style='display:flex;justify-content:center;align-items:center;margin-top:14px;width:100%;'> <a href='http://localhost:8000/u/reset_pswd/"+ encoded_text +"' style='padding:15px;width:auto;color:white;background:#019875;outline:none;text-decoration:none;border-radius:5px;font-size:15px;'> Reset My Password </a></div><br><br></p></div><br><br><p style='font-size:15px;margin:auto;width:fit-content;'>Than you, <b>Wasche Services.</b></p></div> "
            # print(encoded_text)
            
            # decoded_text = cipher_suite.decrypt(encoded_text)
            send_mail_to_client(email,"Password Reset Link","Hello,\n>We recieved a request to reset your password.\n\nClick or paste the link in your browser in order to reset your password.\nNote : </b>This link will expire in another 60 minutes.\n\nlocalhost:8000/u/reset_pswd/"+ encoded_text +"\n\n\nThank you. Wasche Services.",msg)
                # print("present")
            
            pr = Password_Reset(email=up,uuid_id=encoded_text)
            pr.save() 
                # for i in pr:
                #     dif =  str(datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p") - i.date_sent)
                #     dif = dif.split(":")
                #     if int(dif[0]) >= 1 and int(dif[0])>0:
                #         print("exceeded") 
                #     else:
                #         print("still valid")
                # except:
                #     print("sss")
            print("completed addding")
            data['s']=True
            
        except ValidationError:
            print("val")
            data['ef'] = True
        except SMTPException:
            print("msil")
            data['s']=False
        except ValueError:
            print("inn")
            data['inem']=True
        except:
            data['c']=False
    except:
        data['c']=False
    response=HttpResponse(json.dumps(data))

    return response



# from cryptography.fernet import Fernet
# import base64
# import logging
# import traceback
# from django.conf import settings

# #this is your "password/ENCRYPT_KEY". keep it in settings.py file
# #key = Fernet.generate_key() 

# def encrypt(txt):
#     try:
#         # convert integer etc to string first
#         txt = str(txt)
#         # get the key from settings
#         cipher_suite = Fernet(settings.ENCRYPT_KEY) # key should be byte
#         # #input should be byte, so convert the text to byte
#         encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
#         # encode to urlsafe base64 format
#         encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii") 
#         return encrypted_text
#     except Exception as e:
#         # log the error if any
#         logging.getLogger("error_logger").error(traceback.format_exc())
#         return None


# def decrypt(txt):
#     try:
#         # base64 decode
#         txt = base64.urlsafe_b64decode(txt)
#         cipher_suite = Fernet(settings.ENCRYPT_KEY)
#         decoded_text = cipher_suite.decrypt(txt).decode("ascii")     
#         return decoded_text
#     except Exception as e:
#         # log the error
#         logging.getLogger("error_logger").error(traceback.format_exc())
#         return "Error"



# password_validators_help_text_html = _password_validators_help_text_html(password="1234")
# from bs4 import BeautifulSoup
# result = BeautifulSoup(password_validators_help_text_html)

# print(password_validators_help_text_html)
# print()
# print(result)
# class MinimumLengthValidator:
#     """
#     Validate whether the password is of a minimum length.
#     """
#     def __init__(self, min_length=8):
#         self.min_length = min_length

#     def validate(self, password, user=None):
#         if len(password) < self.min_length:
#             raise ValidationError(
#                 ngettext(
#                     "This password is too short. It must contain at least %(min_length)d character.",
#                     "This password is too short. It must contain at least %(min_length)d characters.",
#                     self.min_length
#                 ),
#                 code='password_too_short',
#                 params={'min_length': self.min_length},
#             )

#     def get_help_text(self):
#         return ngettext(
#             "Your password must contain at least %(min_length)d character.",
#             "Your password must contain at least %(min_length)d characters.",
#             self.min_length
#         ) % {'min_length': self.min_length}



# class UserAttributeSimilarityValidator:
#     """
#     Validate whether the password is sufficiently different from the user's
#     attributes.

#     If no specific attributes are provided, look at a sensible list of
#     defaults. Attributes that don't exist are ignored. Comparison is made to
#     not only the full attribute value, but also its components, so that, for
#     example, a password is validated against either part of an email address,
#     as well as the full address.
#     """
#     DEFAULT_USER_ATTRIBUTES = ('username', 'first_name', 'last_name', 'email')

#     def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7):
#         self.user_attributes = user_attributes
#         self.max_similarity = max_similarity

#     def validate(self, password, user=None):
#         if not user:
#             return

#         for attribute_name in self.user_attributes:
#             value = getattr(user, attribute_name, None)
#             if not value or not isinstance(value, str):
#                 continue
#             value_parts = re.split(r'\W+', value) + [value]
#             for value_part in value_parts:
#                 if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
#                     try:
#                         verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
#                     except FieldDoesNotExist:
#                         verbose_name = attribute_name
#                     raise ValidationError(
#                         _("The password is too similar to the %(verbose_name)s."),
#                         code='password_too_similar',
#                         params={'verbose_name': verbose_name},
#                     )

#     def get_help_text(self):
#         return _("Your password can't be too similar to your other personal information.")



# class CommonPasswordValidator:
#     """
#     Validate whether the password is a common password.

#     The password is rejected if it occurs in a provided list of passwords,
#     which may be gzipped. The list Django ships with contains 20000 common
#     passwords (lowercased and deduplicated), created by Royce Williams:
#     https://gist.github.com/roycewilliams/281ce539915a947a23db17137d91aeb7
#     The password list must be lowercased to match the comparison in validate().
#     """
#     DEFAULT_PASSWORD_LIST_PATH = Path(__file__).resolve().parent / 'common-passwords.txt.gz'

#     def __init__(self, password_list_path=DEFAULT_PASSWORD_LIST_PATH):
#         try:
#             with gzip.open(str(password_list_path)) as f:
#                 common_passwords_lines = f.read().decode().splitlines()
#         except IOError:
#             with open(str(password_list_path)) as f:
#                 common_passwords_lines = f.readlines()

#         self.passwords = {p.strip() for p in common_passwords_lines}

#     def validate(self, password, user=None):
#         if password.lower().strip() in self.passwords:
#             raise ValidationError(
#                 _("This password is too common."),
#                 code='password_too_common',
#             )

#     def get_help_text(self):
#         return _("Your password can't be a commonly used password.")



# class NumericPasswordValidator:
#     """
#     Validate whether the password is alphanumeric.
#     """
#     def validate(self, password, user=None):
#         if password.isdigit():
#             raise ValidationError(
#                 _("This password is entirely numeric."),
#                 code='password_entirely_numeric',
#             )

#     def get_help_text(self):
#         return _("Your password can't be entirely numeric.")
