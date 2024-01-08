from django.contrib import admin
from .models import *

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user_profile',)

class CartProductInline(admin.TabularInline):
    model = CartProduct
    extra = 1

@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')

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


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('type',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description', 'date')
    search_fields = ('name', 'description')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'date_created')

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1  # Количество пустых форм для добавления