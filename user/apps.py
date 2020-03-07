from django.apps import AppConfig

class UserConfig(AppConfig):
    name = 'user'
    def ready(self):
        print("called")

        from user.signals import pre_delete_user,post_save_user,post_save_executive
        from django.db.models.signals import pre_save,post_save
        from user.models import User
        from delivery_executives.models import Deliver_Executive
        post_save.connect(post_save_user,sender=User)
        print("added")
        post_save.connect(post_save_executive,sender=Deliver_Executive)
