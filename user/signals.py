from user.models import Removed_Users,User
from dashboard.models import Order_DashBoard
def pre_delete_user(sender,instance,**kwargs):
    ru = Removed_Users(email=str(instance))
    ru.save()
    print('{instance} was deleted'.format(instance=str(instance)))
def post_save_user(sender,instance,**kwargs):
    
    u = User.objects.get(email = str(instance))
    if not Order_DashBoard.objects.filter(email = u).exists():
        o = Order_DashBoard(email=u)
        o.save()
        print('Dashboard for {instance} was Created'.format(instance=str(instance)))
