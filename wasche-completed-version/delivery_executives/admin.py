from django.contrib import admin
from django.utils.html import format_html
from .models import Deliver_Executive,ongoing_delivery
# Register your models here.
@admin.register(Deliver_Executive)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'contract_name',
        
        'phone_number',
        'address',
        'account_actions',
    )
    
    def account_actions(self, obj):
        # print(dir(obj))
        # print(obj.pk)
        text_html = '<a class="button" download="{}-Qr-Code.png" href="{}">Download Qr Code</a>'.format(obj.name,bytes(obj.qr_code_data).decode('utf-8'))
        return format_html(
            text_html
        )
    account_actions.short_description = 'Account Actions'
    account_actions.allow_tags = True
@admin.register(ongoing_delivery)
class OnGoingDelivery(admin.ModelAdmin):
    list_display = (
        
        'name',
        'on_going',
        'date_started',
    )
    
