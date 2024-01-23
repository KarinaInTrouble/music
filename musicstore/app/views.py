from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.urls import reverse
from django.contrib import messages
from django.db.models import Max, Min, Avg, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .forms import *

# Create your views here.

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()

    # Возвращаем HttpResponse или render для GET-запроса
    return render(request, 'registration/register.html', {'form': form})

@login_required
def client(request):
    categories = Category.objects.all()
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('client')  # Используйте redirect для перенаправления
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'client.html', {'user_profile': user_profile, 'categories': categories, 'form': form})

@login_required
def edit_client_profile(request):
    categories = Category.objects.all()
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('client')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_client_profile.html', {'form': form, 'categories': categories})

def index(request):
    categories = Category.objects.all()
    action_category = NewsCategory.objects.get(type='Акции')
    action_news = News.objects.filter(category=action_category).order_by('-date')[:4]
    latest_news = News.objects.order_by('-date')[:4]
    return render(request, 'index.html', {'latest_news': latest_news, 'categories': categories,'action_news': action_news})

def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    return render(request, 'news_detail.html', {'news_item': news_item})

def manager(request):
    categories = Category.objects.all()
    return render(request, 'manager.html', {'categories': categories})


def brand_list(request):
    categories = Category.objects.all()
    all_brands = Manufacturer.objects.all()
    form = ManufacturerForm()

    paginator = Paginator(all_brands, 9)
    page = request.GET.get('page')

    try:
        brands = paginator.page(page)
    except PageNotAnInteger:
        brands = paginator.page(1)
    except EmptyPage:
        brands = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = ManufacturerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('brand_list')

    return render(request, 'brands.html', {'brands': brands, 'categories': categories, 'form': form})

def brand_edit(request, brand_id):
    categories = Category.objects.all()
    brand = get_object_or_404(Manufacturer, id=brand_id)

    if request.method == 'POST':
        form = ManufacturerForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            return redirect('brand_list')

    form = ManufacturerForm(instance=brand)
    return render(request, 'brand_edit.html', {'form': form, 'brand': brand, 'categories': categories})

def brand_delete(request, brand_id):
    brand = get_object_or_404(Manufacturer, id=brand_id)
    brand.delete()
    return redirect('brand_list')

def product_list(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=category_id)
    subcategories = Subcategory.objects.filter(category=category)
    manufacturers = Manufacturer.objects.all()
    products = Product.objects.filter(category=category)
    max_range = products.aggregate(Max('price'))['price__max']
    min_range = products.aggregate(Min('price'))['price__min']

    # Фильтрация по подкатегории
    subcategory_id = request.GET.get('subcategory')
    if subcategory_id:
        products = products.filter(subcategory_id=subcategory_id)

    # Фильтрация по производителю
    manufacturer_id = request.GET.get('manufacturer')
    if manufacturer_id:
        products = products.filter(brand_id=manufacturer_id)

    # Фильтрация по цене
    max_price = request.GET.get('price')
    if max_price:
        products = products.filter(price__lte=max_price)
    
    
    paginator = Paginator(products, 9)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # Если параметр страницы не является целым числом, показать первую страницу
        products = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше максимального, показать последнюю страницу
        products = paginator.page(paginator.num_pages)

    return render(request,'product_list.html', 
                {'categories': categories, 
                 'category': category, 
                 'subcategories': subcategories, 
                 'manufacturers': manufacturers, 
                 'products': products,
                 'max_range': max_range,
                 'min_range': min_range})

def edit_catalog(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list', category_id=product.category.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_catalog.html', {'form': form, 'product': product})

def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    category_id = product.category.id
    product.delete()
    return redirect('product_list', category_id=category_id)


@login_required
def product_detail(request, product_id):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(subject=product)
    is_favorite = Favorite.objects.filter(subject=product, user=request.user).exists()
    average_rating = reviews.aggregate(Avg('stars'))['stars__avg']

    return render(request, 'product_detail.html', {'categories': categories,'product': product, 'reviews': reviews, 'is_favorite': is_favorite, "average_rating": average_rating})

@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Проверяем, не добавлен ли уже товар в избранное
    if not Favorite.objects.filter(subject=product, user=request.user).exists():
        Favorite.objects.create(subject=product, user=request.user)

    return redirect('product_list', category_id=product.category.id)

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        stars = request.POST.get('stars')
        
        Review.objects.create(subject=product, user=request.user, feedback=feedback, stars=stars)

    return redirect('product_detail', product_id=product_id)

def add_product(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    # Добавляем пагинацию
    paginator = Paginator(products, 10)
    page = request.GET.get('page', 1)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_product')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form, 'products': products, 'categories': categories})


def add_news(request):
    categories = Category.objects.all()
    news_list = News.objects.all()

    # Добавляем пагинацию
    paginator = Paginator(news_list, 5)
    page = request.GET.get('page')

    try:
        news_list = paginator.page(page)
    except PageNotAnInteger:
        news_list = paginator.page(1)
    except EmptyPage:
        news_list = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_news')
    else:
        form = NewsForm()

    return render(request, 'add_news.html', {'form': form, 'news_list': news_list, 'categories': categories})

def edit_news(request, news_id):
    categories = Category.objects.all()
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('add_news')
    else:
        form = NewsForm(instance=news)
    return render(request, 'edit_news.html', {'form': form, 'news': news, 'categories': categories})

def delete_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    news.delete()
    return redirect('add_news')

def all_orders(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'all_orders.html', context)

#Клиент

@login_required
def favorites(request):
    categories = Category.objects.all()
    user = request.user
    favorites = Favorite.objects.filter(user=user)
    return render(request, 'favorites.html', {'categories': categories,'favorites': favorites})

@login_required
def reviews(request):
    categories = Category.objects.all()
    user = request.user
    all_reviews = Review.objects.filter(user=user)

    paginator = Paginator(all_reviews, 10)
    page = request.GET.get('page')

    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)

    return render(request, 'reviews.html', {'categories': categories, 'reviews': reviews})


#Заказы

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    # Проверяем, существует ли корзина у пользователя
    try:
        cart = user_profile.cart
    except Cart.DoesNotExist:
        # Если нет, создаем новую корзину
        cart = Cart.objects.create(user_profile=user_profile)

    # Далее ваш код добавления товара в корзину
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)

    if not created:
        if cart_product.quantity < product.quantity:
            cart_product.quantity += 1
            cart_product.save()
        else:
            messages.warning(request, f"{product.name} is out of stock.")
    
    return redirect('product_list', category_id=product.category.id)

@login_required
def view_cart(request):
    categories = Category.objects.all()
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    try:
        cart = user_profile.cart
        cart_products = CartProduct.objects.filter(cart=cart)
        total_price = sum(cart_product.product.price * cart_product.quantity for cart_product in cart_products)
    except Cart.DoesNotExist:
        cart_products = []
        total_price = 0

    context = {'cart_products': cart_products, 'user_profile': user_profile, 'total_price': total_price, 'categories':categories}
    return render(request, 'view_cart.html', context)

@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    try:
        cart = user_profile.cart
    except Cart.DoesNotExist:
        return redirect('product_list', category_id=product.category.id)

    cart_product = CartProduct.objects.filter(cart=cart, product=product).first()

    if cart_product and cart_product.quantity > 1:
        cart_product.quantity -= 1
        cart_product.save()
    elif cart_product:
        cart_product.delete()

    return redirect('product_list', category_id=product.category.id)

@login_required
def checkout(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Создаем заказ в базе данных
            order = Order(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                phone_number=form.cleaned_data['phone_number'],
                email=form.cleaned_data['email'],
                delivery_address=form.cleaned_data['delivery_address'],
                comments=form.cleaned_data['comments'],
                payment_choices=form.cleaned_data['payment_choices']
            )
            order.save()

            # Добавим продукты из корзины к заказу
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                cart = user_profile.cart
                cart_products = CartProduct.objects.filter(cart=cart)
                total_price = 0

                for cart_product in cart_products:
                    order_product = OrderProduct(order=order, product=cart_product.product, quantity=cart_product.quantity)
                    order_product.save()
                    total_price += cart_product.product.price * cart_product.quantity

                order.total_price = total_price
                order.save()

                # Опционально, очистим корзину после создания заказа
                cart.products.clear()

                # Перенаправляем пользователя после успешной обработки
                return redirect('client')
            except UserProfile.DoesNotExist:
                # Обработка ситуации, когда у пользователя нет профиля
                messages.warning(request, "Your profile is missing.")
                return redirect('checkout')
            except Cart.DoesNotExist:
                # Обработка ситуации, когда у пользователя нет корзины
                messages.warning(request, "Your cart is empty.")
                return redirect('checkout')
    else:
        form = OrderForm()

    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
        cart = user_profile.cart
        cart_products = CartProduct.objects.filter(cart=cart)
        total_price = sum(cart_product.product.price * cart_product.quantity for cart_product in cart_products)
    except UserProfile.DoesNotExist:
        user_profile = None
        cart_products = []
        total_price = 0

    context = {'form': form, 'user_profile': user_profile, 'cart_products': cart_products, 'total_price': total_price}
    return render(request, 'checkout.html', context)

@login_required
def user_orders(request):
    categories = Category.objects.all()
    user = request.user
    orders = Order.objects.filter(user=user)
    
    context = {'user': user, 'orders': orders, 'categories':categories}
    return render(request, 'user_orders.html', context)

def all_orders(request):
    users = UserProfile.objects.all()
    categories = Category.objects.all()
    orders = Order.objects.all() 
    context = {'orders': orders, 'categories':categories, 'users':users}
    return render(request, 'all_orders.html', context)