from django.contrib import admin
from .models import Tracker
# Register your models here.
# admin.site.register(Tracker)
@admin.register(Tracker)
class Tracking(admin.ModelAdmin):
    list_display = (
        'track_id',
        'type_op',
        'on_going',
        'date',
        'time',
        'completed_status',
        'created_date',
        'completion_date',
    )
    