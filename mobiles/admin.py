from django.contrib import admin
from .models import RepairBooking, Accessory


@admin.register(RepairBooking)
class RepairBookingAdmin(admin.ModelAdmin):

    list_display = (
        'customer_name',
        'phone_number',
        'mobile_brand',
        'mobile_model',
        'problem_type',
        'status',
        'final_cost',
        'amount_paid',
        'payment_status',
        'payment_method',
        'preferred_date',
    )

    search_fields = (
        'customer_name',
        'phone_number',
        'mobile_brand',
        'mobile_model',
    )

    list_filter = (
        'status',
        'payment_status',
        'payment_method',
        'mobile_brand',
        'visit_type',
        'preferred_date',
    )

    list_editable = (
        'status',
        'final_cost',
        'amount_paid',
        'payment_status',
        'payment_method',
    )

    ordering = ('-preferred_date',)


@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'category',
        'price',
        'stock',
        'created_at',
    )

    search_fields = (
        'name',
        'category',
    )

    list_filter = (
        'category',
    )

    list_editable = (
        'price',
        'stock',
    )

    ordering = ('-created_at',)