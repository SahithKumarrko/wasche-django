from django.contrib import admin
from application.models import Contact,Subscribers,Plans
# Register your models here.
@admin.register(Plans)
class User_Plans(admin.ModelAdmin):
    list_display = (
        'user',
        'plan',
        'current_order_id',
        'date_created',
        'end_date',
        'extra_amount',
        'regular_count',
        'other_count',
        'remaining_amount',
        'eligibility',

    )
    
@admin.register(Contact)
class Contact_Info(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'subject',
        'message',
        'date_sent',
    )
    
@admin.register(Subscribers)
class Subscribers_Details(admin.ModelAdmin):
    list_display = (
        'email',
        'date_subscribed',
    )
    
# admin.site.register(Contact)
# admin.site.register(Subscribers)
# admin.site.register(Plans)
