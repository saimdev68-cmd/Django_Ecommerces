from django.contrib import admin
from .models import Category, Brand, Product , Slider 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]
    prepopulated_fields = {"slug":("name",)}
    list_filter = ["is_active"]
    search_fields = ["name"]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]
    list_filter = ["is_active", "category"]
    prepopulated_fields = {"slug":("name",)}
    search_fields = ["name",]
    filter_horizontal = ["category"]

class SliderInline(admin.TabularInline):
    model = Slider
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [SliderInline]
    list_display = [
        "name",
        "price",
        "stock",
        "is_active",
        "is_published"
    ]
    prepopulated_fields = {"slug":("name",)}
    list_filter = [
        "is_active",
        'is_trending',
        'is_promotional',
        "is_published",
        "category",
        "brand",
    ]
    search_fields = ["name"]