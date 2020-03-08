from django.contrib import admin
# Register your models here.
from .models import Transaction
# admin.site.register(Transaction)
@admin.register(Transaction)
class Transactions(admin.ModelAdmin):
    list_display = (
        'order_id',
        'plan',
        'amount',
        'referenceId',
        'customer_name',
        'customer_email',
        'customer_phone_number',
        'eligibility',
        'completed_status',
        'transaction_date',
    )
    