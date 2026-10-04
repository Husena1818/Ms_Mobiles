from django.contrib import admin
from .models import Mobile, Order, RepairRequest


@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "brand",
        "model",
        "price",
        "stock",
    )

    list_filter = (
        "brand",
    )

    search_fields = (
        "name",
        "brand",
        "model",
    )

    ordering = (
        "id",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_id",
        "customer_name",
        "phone",
        "mobile",
        "quantity",
        "total_amount",
        "status",
        "order_date",
    )

    list_filter = (
        "status",
        "order_date",
    )

    search_fields = (
        "order_id",
        "customer_name",
        "phone",
        "email",
    )

    ordering = (
        "-order_date",
    )

    readonly_fields = (
        "order_date",
    )


@admin.register(RepairRequest)
class RepairRequestAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer_name",
        "phone",
        "brand",
        "mobile_model",
        "service",
        "problem_description",
        "status",
        "request_date",
    )

    list_filter = (
        "status",
        "service",
        "request_date",
    )

    search_fields = (
        "customer_name",
        "phone",
        "brand",
        "mobile_model",
        "problem_description",
    )

    readonly_fields = (
        "request_date",
    )

    ordering = (
        "-request_date",
    )