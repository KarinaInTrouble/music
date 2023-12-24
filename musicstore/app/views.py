from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
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

def client(request):
    categories = Category.objects.all()
    return render(request, 'client.html', {'categories': categories})

def product_list(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=category_id)
    subcategories = Subcategory.objects.filter(category=category)
    manufacturers = Manufacturer.objects.all()
    products = Product.objects.filter(category=category)

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

    return render(request, 'product_list.html', {'categories': categories, 'category': category, 'subcategories': subcategories, 'manufacturers': manufacturers, 'products': products})

@login_required
def product_detail(request, product_id):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(subject=product)
    is_favorite = Favorite.objects.filter(subject=product, user=request.user).exists()

    return render(request, 'product_detail.html', {'categories': categories,'product': product, 'reviews': reviews, 'is_favorite': is_favorite})

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

