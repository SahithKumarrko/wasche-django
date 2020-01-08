from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from contracts.models import Contracts
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
    profile_image = models.ImageField(upload_to='pics',blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'address', 'phone_number', 'zip_code','gender']
    
    objects = UserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('user_detail', kwargs={'pk': self.pk})
    # def get_full_name(self):
    # def save(self, *args, **kwargs):
    #     # date = timezone.now()
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
    
    class Meta:
        verbose_name_plural = "Password Resets"
    def save(self, *args, **kwargs):
        if not self.id:
            self.date_sent = timezone.now()
        return super(Password_Reset,self).save(*args,**kwargs)

class Removed_Users(models.Model):
    email       = models.EmailField()
    date_removed = models.DateTimeField(editable=False)
    
    class Meta:
        verbose_name_plural = "Removed Users"
    def save(self, *args, **kwargs):
        if not self.id:
            self.date_removed = timezone.now()
        return super(Removed_Users,self).save(*args,**kwargs)