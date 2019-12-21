from user.models import Removed_Users
def pre_delete_user(sender,instance,**kwargs):
    ru = Removed_Users(email=str(instance))
    ru.save()
    print('{instance} was deleted'.format(instance=str(instance)))
