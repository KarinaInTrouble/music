from django.contrib import admin
from .models import *
# Register your models here.

from django.contrib import admin
from .models import Category, Subcategory, Manufacturer, Product, Review, Favorite, Order, OrderItem, OrderProcessing, NewsCategory, News

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'name')

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory', 'brand', 'price', 'quantity')
    search_fields = ('name', 'brand')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'feedback', 'stars')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'order_date')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')

@admin.register(OrderProcessing)
class OrderProcessingAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'processing_date')

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('type',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description', 'date')
    search_fields = ('name', 'description')
