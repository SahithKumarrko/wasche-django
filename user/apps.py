from django.apps import AppConfig

class UserConfig(AppConfig):
    name = 'user'
    def ready(self):
        print("called")

        # from user.signals import pre_delete_user
        # from django.db.models.signals import pre_delete
        # from user.models import User
        # pre_delete.connect(pre_delete_user,sender=User)
        # print("added")
