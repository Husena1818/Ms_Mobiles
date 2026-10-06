from django.contrib import admin
from .models import RepairBooking, Accessory


@admin.register(RepairBooking)
class RepairBookingAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'customer_name',
        'phone_number',
        'mobile_brand',
        'mobile_model',
        'problem_type',
        'visit_type',
        'status',
        'final_cost',
        'amount_paid',
        'balance_due',
        'payment_status',
        'preferred_date',
    )

    search_fields = (
        'customer_name',
        'phone_number',
        'customer_email',
        'mobile_brand',
        'mobile_model',
        'problem_type',
    )

    list_filter = (
        'status',
        'payment_status',
        'payment_method',
        'visit_type',
        'mobile_brand',
        'preferred_date',
    )

    list_editable = (
        'status',
        'final_cost',
        'amount_paid',
        'payment_status',
    )

    readonly_fields = (
        'id',
        'created_at',
        'balance_due',
    )

    fieldsets = (
        (
            'Customer Information',
            {
                'fields': (
                    'customer_name',
                    'customer_email',
                    'phone_number',
                )
            }
        ),
        (
            'Device Information',
            {
                'fields': (
                    'mobile_brand',
                    'mobile_model',
                    'problem_type',
                    'problem_description',
                    'phone_image',
                )
            }
        ),
        (
            'Repair Details',
            {
                'fields': (
                    'visit_type',
                    'preferred_date',
                    'status',
                )
            }
        ),
        (
            'Payment Information',
            {
                'fields': (
                    'estimated_cost',
                    'final_cost',
                    'amount_paid',
                    'balance_due',
                    'payment_status',
                    'payment_method',
                    'payment_date',
                )
            }
        ),
        (
            'System Information',
            {
                'fields': (
                    'id',
                    'created_at',
                )
            }
        ),
    )

    ordering = ('-created_at',)


@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'category',
        'price',
        'stock',
        'created_at',
    )

    search_fields = (
        'name',
        'category',
        'description',
    )

    list_filter = (
        'category',
    )

    list_editable = (
        'price',
        'stock',
    )

    readonly_fields = (
        'id',
        'created_at',
    )

    fieldsets = (
        (
            'Accessory Information',
            {
                'fields': (
                    'name',
                    'category',
                    'description',
                    'image',
                )
            }
        ),
        (
            'Stock & Pricing',
            {
                'fields': (
                    'price',
                    'stock',
                )
            }
        ),
        (
            'System Information',
            {
                'fields': (
                    'id',
                    'created_at',
                )
            }
        ),
    )

    ordering = ('-created_at',)