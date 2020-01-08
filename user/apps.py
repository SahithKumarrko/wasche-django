from django.apps import AppConfig

class UserConfig(AppConfig):
    name = 'user'
    def ready(self):
        print("called")

        from user.signals import pre_delete_user,post_save_user
        from django.db.models.signals import pre_save,post_save
        from user.models import User
        post_save.connect(post_save_user,sender=User)
        print("added")
