from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.db import models
from django.utils.translation import ugettext_lazy as _
# from django.utils import timezone
from wasche.custom_settings import settings
from contracts.models import Contracts
from datetime import datetime
import base64
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    username    = None
    first_name  = models.CharField(max_length=254, blank=False)
    last_name = models.CharField(max_length=254, blank=True)
    email       = models.EmailField(_('email address'),blank=False, unique=True)
    address    = models.CharField(max_length=254, blank=False)
    phone_number    = models.CharField(max_length=20, blank=False)
    zip_code   = models.CharField(max_length=20, blank=False)
    contract_name = models.ForeignKey(Contracts,default="No College",on_delete = models.CASCADE)
    gender     = models.CharField(max_length=8, blank=False)
    subscription_plan = models.CharField(max_length=4,default='off')
    news_letter_subscription = models.CharField(max_length=4,default='off')
    # profile_image = models.ImageField(upload_to='pics',blank=True)
    profile_image = models.CharField(max_length=254,default="No")
    USERNAME_FIELD = 'email'
    qr_code_data = models.BinaryField()
    
    # def set_data(self,data):
    #     self._qr_code_data = data
    # def get_data(self,data):
    #     return self._qr_code_data
    # qr_code_data = property(get_data,set_data)

    REQUIRED_FIELDS = ['first_name', 'address', 'phone_number', 'zip_code','gender']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('user_detail', kwargs={'pk': self.pk})
    # def get_full_name(self):
    # def save(self, *args, **kwargs):
    #     # date = datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
    #     # ood = Overflown_Orders_Data(email=self.email,overflown_data=self.ordered_dates)
    #     # ood.save()
    #     from dashboard.models import Order_DashBoard
            
    #     if not self.id:
    #         print("Created new date for user")
    #         o = Order_DashBoard(email=self.email)
    #         o.save()
    #     return super(User,self).save(*args,**kwargs)
    
    #     """
    #     Returns the first_name plus the last_name, with a space in between.
    #     """
    #     full_name = '%s %s' % (self.first_name, self.last_name)
    #     return full_name.strip()
        
    # def get_short_name(self):
    #     "Returns the short name for the user."
    #     return self.first_name

    # def email_user(self, subject, message, from_email=None):
    #     """
    #     Sends an email to this User.
    #     """
    #     send_mail(subject, message, from_email, [self.email])    

class Password_Reset(models.Model):
    email       = models.ForeignKey(User,default=1, on_delete=models.CASCADE)
    uuid_id  = models.CharField(max_length=200,default="")
    date_sent = models.DateTimeField(editable=False)
    def __str__(self):
        return self.email.email

    class Meta:
        verbose_name_plural = "Password Resets"
    def save(self, *args, **kwargs):
        if not self.id:
            self.date_sent = datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
        return super(Password_Reset,self).save(*args,**kwargs)

class Removed_Users(models.Model):
    email       = models.EmailField()
    date_removed = models.DateTimeField(editable=False)
    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Removed Users"
    def save(self, *args, **kwargs):
        if not self.id:
            self.date_removed = datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
        return super(Removed_Users,self).save(*args,**kwargs)

class OneSignal(models.Model):
    email       = models.ForeignKey(User,default="wasche.services@gmail.com",on_delete=models.CASCADE)
    pid = models.CharField(max_length=254,default="")
    enabled = models.BooleanField(default=True)
    type_os = models.CharField(max_length=254,default="")
    date_created = models.DateTimeField(editable=False)
    def __str__(self):
        return self.email.email

    class Meta:
        verbose_name_plural = "Onesignal Data"
    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
        return super(OneSignal,self).save(*args,**kwargs)

class Notifications(models.Model):
    type_msg = models.CharField(max_length=254,default="notify")
    email       = models.ForeignKey(User,default="wasche.services@gmail.com",on_delete=models.CASCADE)
    sent_from = models.CharField(max_length=254,default="")
    title = models.CharField(max_length=254,default="")
    msg = models.CharField(max_length=1000,default="")
    seen = models.BooleanField(default=False)
   
   
    date_created = models.DateTimeField(editable=False)
    # REQUIRED_FIELDS = ["email","sent_from","title","msg","seen"]
    def __str__(self):
        return "From : " + self.sent_from + " , to  :  " + self.email.email

    class Meta:
        verbose_name_plural = "Notifications"
    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = datetime.strptime(datetime.now(tz=settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
        return super(Notifications,self).save(*args,**kwargs)

