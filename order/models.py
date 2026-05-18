from django.db import models
from accounts.models import CustomUser
from products.models import Product

# Create your models here.

class Order(models.Model):
    STATUS_CHOICE = [
        ("pending","pending"),
        ("shipped","shipped"),
        ("out for delivery","out for delivery"),
        ("Delivered","Delivered")
    ]
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=13)
    address = models.TextField()
    stripe_session_id = models.CharField(max_length=255,null=True,blank=True)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=100,choices=STATUS_CHOICE,default="pending")
    grand_total = models.DecimalField(max_digits=8,decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - Order # {self.id}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product.name
