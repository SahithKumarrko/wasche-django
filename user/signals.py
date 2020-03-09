from user.models import Removed_Users,User
from dashboard.models import Order_DashBoard
from application.models import Plans
import pyqrcode
import json
def pre_delete_user(sender,instance,**kwargs):
    ru = Removed_Users(email=str(instance))
    ru.save()
    print('{instance} was deleted'.format(instance=str(instance)))
def post_save_user(sender,instance,**kwargs):
    
    u = User.objects.get(email = str(instance))
    if not Plans.objects.filter(user = u).exists():
        o = Plans(user=u)
        o.save()
        print('Plans for {instance} was Created'.format(instance=str(instance)))

    if not Order_DashBoard.objects.filter(email = u).exists():
        o = Order_DashBoard(email=u)
        o.save()
        print('Dashboard for {instance} was Created'.format(instance=str(instance)))
def post_save_executive(sender,instance,**kwargs):
    if(len(instance.qr_code_data)==0):
        print("Creating qr code : {} => {}".format(instance.id,instance.name))
        try:
            qr = pyqrcode.create(json.dumps({"wasche-services":{"name":instance.name,"id":instance.id}}))
            print(qr)
            dta = "data:image/png;base64," + qr.png_as_base64_str()
            print("Data : ",dta)
            instance.qr_code_data = bytes(dta,'utf-8')
            print("Completed")
            instance.save()
        except Exception as exp:
            print("Errorr at de :  ",exp)
    
    
