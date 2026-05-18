from django.db import models
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Brand(models.Model):
    category = models.ManyToManyField(Category,related_name="brands")
    name = models.CharField(max_length=255,null=True)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to="brand/",blank=True,null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name="products")
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,related_name="products")
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="product/",null=True,blank=True)
    is_published = models.BooleanField(default=False)
    is_promotional = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True,blank=True)

    class Meta:
        ordering = ["-published_at"]

    def save(self, *args, **kwargs):
        if self.is_published:
            if self.published_at is None:
                self.published_at = timezone.now()
        else:
            self.published_at = None
        super().save(*args, **kwargs)

class Slider(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE,related_name="slider")
    image = models.ImageField(upload_to="product/slider/")

    def __str__(self):
        return self.product.name
    