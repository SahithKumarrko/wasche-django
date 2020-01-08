from django.contrib import admin
from dashboard.models import Order_DashBoard, Old_Orders

admin.site.register(Order_DashBoard)
# admin.site.register(Overflown_Orders_Data)

admin.site.register(Old_Orders)

# Register your models here.
