from django.db import models


class RepairBooking(models.Model):

    STATUS_CHOICES = [
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Diagnosis', 'Diagnosis'),
        ('In Progress', 'In Progress'),
        ('Quality Check', 'Quality Check'),
        ('Ready', 'Ready'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    VISIT_CHOICES = [
        ('Shop Visit', 'Shop Visit'),
        ('Pickup', 'Pickup'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Partially Paid', 'Partially Paid'),
        ('Paid', 'Paid'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
        ('Card', 'Card'),
        ('Other', 'Other'),
    ]

    customer_name = models.CharField(
        max_length=150
    )

    customer_email = models.EmailField(
        max_length=254,
        blank=True,
        null=True
    )

    phone_number = models.CharField(
        max_length=15
    )

    mobile_brand = models.CharField(
        max_length=100
    )

    mobile_model = models.CharField(
        max_length=100
    )

    problem_type = models.CharField(
        max_length=150
    )

    problem_description = models.TextField()

    phone_image = models.ImageField(
        upload_to='repair_phones/',
        blank=True,
        null=True
    )

    visit_type = models.CharField(
        max_length=20,
        choices=VISIT_CHOICES,
        default='Shop Visit'
    )

    preferred_date = models.DateField()

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='New'
    )

    estimated_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    final_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending'
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True,
        null=True
    )

    payment_date = models.DateTimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    @property
    def balance_due(self):
        final = self.final_cost or 0
        paid = self.amount_paid or 0
        return final - paid

    def __str__(self):
        return f"{self.customer_name} - {self.mobile_model}"


class Accessory(models.Model):

    CATEGORY_CHOICES = [
        ('Covers & Pouches', 'Covers & Pouches'),
        ('Chargers', 'Chargers'),
        ('Cables', 'Cables'),
        ('Tempered Glass', 'Tempered Glass'),
        ('Earphones & Earbuds', 'Earphones & Earbuds'),
        ('Power Banks', 'Power Banks'),
        ('Mobile Holders', 'Mobile Holders'),
        ('Other', 'Other'),
    ]

    name = models.CharField(
        max_length=200
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField(
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    image = models.ImageField(
        upload_to='accessories/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name