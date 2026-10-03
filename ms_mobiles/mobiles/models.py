from django.db import models
from django.contrib.auth.models import User


class Mobile(models.Model):
    brand = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ram = models.CharField(max_length=50)
    storage = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='mobiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.model_name}"


class Repair(models.Model):
    STATUS_CHOICES = [
        ('Received', 'Received'),
        ('Diagnosing', 'Diagnosing'),
        ('Repairing', 'Repairing'),
        ('Quality Check', 'Quality Check'),
        ('Ready for Pickup', 'Ready for Pickup'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    ]

    PROBLEM_CHOICES = [
        ('Broken Screen', 'Broken Screen'),
        ('Battery Issue', 'Battery Issue'),
        ('Charging Problem', 'Charging Problem'),
        ('Speaker / Mic', 'Speaker / Mic'),
        ('Software Problem', 'Software Problem'),
        ('Display Problem', 'Display Problem'),
        ('Water Damage', 'Water Damage'),
        ('Motherboard Problem', 'Motherboard Problem'),
        ('Other', 'Other'),
    ]

    SERVICE_TYPE_CHOICES = [
        ('Pickup & Drop-off', 'Pickup & Drop-off'),
        ('Shop Visit', 'Shop Visit'),
    ]

    PART_QUALITY_CHOICES = [
        ('Original', 'Original'),
        ('OEM', 'OEM'),
        ('Compatible', 'Compatible'),
    ]

    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    mobile_brand = models.CharField(max_length=100)
    mobile_model = models.CharField(max_length=100)
    imei_number = models.CharField(max_length=50, blank=True)
    problem_type = models.CharField(
        max_length=50,
        choices=PROBLEM_CHOICES,
        default='Other'
    )
    problem = models.TextField()
    phone_photo = models.ImageField(
        upload_to='repair_photos/',
        blank=True,
        null=True
    )
    service_type = models.CharField(
        max_length=30,
        choices=SERVICE_TYPE_CHOICES,
        default='Shop Visit'
    )
    parts_replaced = models.CharField(max_length=255, blank=True)
    part_quality = models.CharField(
        max_length=20,
        choices=PART_QUALITY_CHOICES,
        blank=True
    )
    technician = models.CharField(max_length=100, blank=True)
    repair_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Received'
    )
    received_date = models.DateTimeField(auto_now_add=True)
    expected_delivery_date = models.DateField(
        null=True,
        blank=True
    )
    delivered_date = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.customer_name} - {self.mobile_brand} {self.mobile_model}"


class Order(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    mobile = models.ForeignKey(
        Mobile,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=30,
        default='Placed'
    )

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"