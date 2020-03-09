from django.contrib import admin
from dashboard.models import Order_DashBoard, Old_Orders
@admin.register(Order_DashBoard)
class OrderDashBoard(admin.ModelAdmin):
    list_display = (
        'email',
        'total_orders',
        'ordered_dates',
        'overflown',
        'recent_date',
        'recent_time',
        'years',
        'date_created',
    )
    
@admin.register(Old_Orders)
class OldOrders(admin.ModelAdmin):
    list_display = (
        'email',
        'data',
        'date_created',
    )
    
# admin.site.register(Order_DashBoard)
# admin.site.register(Overflown_Orders_Data)

# admin.site.register(Old_Orders)

# Register your models here.
