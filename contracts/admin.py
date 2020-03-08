from django.contrib import admin
from .models import Contracts
# Register your models here.
# admin.site.register(Contracts)
@admin.register(Contracts)
class ContractsAdmin(admin.ModelAdmin):
    list_display = (
        'contract_name',
        'contract_address',
        'contract_phone_number',
        'contract_state',
        'contract_zip_code',
        'contract_country',
        'contract_established_date',
    )
    