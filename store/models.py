from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


CATEGORY_CHOICES = [
    ('Fashion & Apparel', 'Fashion & Apparel'),
    (' Electronics', ' Electronics'),
    ('Home & Living', 'Home & Living'),
    ('Food & Beverages', 'Food & Beverages'),
    (' Beauty & Personal Care', ' Beauty & Personal Care'),
    ('Toys, Kids & Baby', 'Toys, Kids & Baby'),
    ('Tools & Hardware', 'Tools & Hardware'),
    ('Automotive', 'Automotive'),
    (' Sports & Outdoors', ' Sports & Outdoors'),
    (' Gaming', ' Gaming'),
    ('Books & Stationery', 'Books & Stationery')
]

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES, default='Home & Living')
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

