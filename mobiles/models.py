from django.db import models


# =========================================================
# MOBILE
# =========================================================

class Mobile(models.Model):

    name = models.CharField(max_length=200)

    brand = models.CharField(max_length=100)

    model = models.CharField(max_length=100)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to="mobiles/",
        blank=True,
        null=True
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return f"{self.brand} {self.model}"


# =========================================================
# ORDER
# =========================================================

class Order(models.Model):

    order_id = models.CharField(
        max_length=50,
        unique=True
    )

    customer_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    mobile = models.ForeignKey(
        Mobile,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=30,
        default="Pending"
    )

    order_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.order_id} - {self.customer_name}"


# =========================================================
# REPAIR REQUEST
# =========================================================

class RepairRequest(models.Model):

    SERVICE_CHOICES = [
        ("SCREEN", "Screen Replacement"),
        ("BATTERY", "Battery Replacement"),
        ("CHARGING", "Charging Repair"),
        ("SPEAKER", "Speaker & Mic Repair"),
        ("SOFTWARE", "Software Service"),
        ("HARDWARE", "Hardware Repair"),
        ("OTHER", "Other"),
    ]

    customer_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15
    )

    brand = models.CharField(
        max_length=100
    )

    mobile_model = models.CharField(
        max_length=100
    )

    service = models.CharField(
        max_length=20,
        choices=SERVICE_CHOICES
    )

    # Existing database column
    service_type = models.CharField(
        max_length=100,
        default=""
    )

    problem_description = models.TextField()

    request_date = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=30,
        default="Pending"
    )

    def __str__(self):
        return f"{self.customer_name} - {self.mobile_model}"