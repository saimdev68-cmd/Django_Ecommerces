from django.db import models
from accounts.models import CustomUser
from products.models import Product

# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
    @property
    def grand_total(self):
        return sum(i.total_price for i in self.items.all())
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name
    
    class Meta:
        unique_together = ("cart","product")

    @property
    def total_price(self):
        return self.product.price * self.quantity 