"""
URL configuration for musicstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index, name='index'),
    path('manager', manager, name='manager'),
    path('news/add/', add_news, name='add_news'),
    path('news/<int:news_id>/edit/', edit_news, name='edit_news'),
    path('news/<int:news_id>/delete/', delete_news, name='delete_news'),
    path('brands/', brand_list, name='brand_list'),
    path('brand/<int:brand_id>/edit/', brand_edit, name='brand_edit'),
    path('brand/<int:brand_id>/delete/', brand_delete, name='brand_delete'),
    path('products/<int:category_id>/', product_list, name='product_list'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('product/<int:product_id>/edit/', edit_catalog, name='product_edit'),
    path('product/<int:product_id>/delete/', product_delete, name='product_delete'),
    path('add_product/', add_product, name='add_product'),
    path('add_to_favorites/<int:product_id>/', add_to_favorites, name='add_to_favorites'),
    path('favorites/<int:favs_id>/delete/', delete_favorites, name='favs_delete'),
    path('add_review/<int:product_id>/', add_review, name='add_review'),
    path('news/<int:pk>/', news_detail, name='news_detail'),
    path('all_orders/', all_orders, name='all_orders'),

    path('favorites', favorites, name='favorites'),
    path('reviews', reviews, name='reviews'),
    path('client', client, name='client'),
    path('edit_client_profile/', edit_client_profile, name='edit_client_profile'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('view_cart/', view_cart, name='view_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('user_orders/', user_orders, name='user_orders'),

    path('register/', registration_view, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
