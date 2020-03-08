from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User,Password_Reset,Removed_Users,OneSignal,Notifications

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','gender','address','phone_number','zip_code','subscription_plan','news_letter_subscription','contract_name','profile_image')}),
        
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name','last_login', 'date_joined','is_active','gender','address','phone_number','zip_code','subscription_plan','news_letter_subscription','contract_name','profile_image', 'is_staff')
    search_fields = ('email', 'last_login', 'date_joined','first_name','is_active', 'last_name','gender','address','phone_number','zip_code','subscription_plan','news_letter_subscription','contract_name','profile_image')
    ordering = ('email',)

@admin.register(Password_Reset)
class PasswordResetAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'uuid_id',
        'date_sent',
    )
    
@admin.register(Removed_Users)
class RemovedUsersAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'date_removed',
    )
    
@admin.register(OneSignal)
class OneSignalAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'pid',
        'enabled',
        'type_os',
        'date_created',
    )
@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'type_msg',
        'sent_from',
        'title',
        'msg',
        'seen',
        'image_url',
        'date_created',
    )
    
# admin.site.register(Password_Reset)

# admin.site.register(Removed_Users)

# admin.site.register(OneSignal)
# admin.site.register(Notifications)