from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField("ФИО", max_length=255, blank=True, null=True)
    photo = models.FileField("Фото", upload_to="profile_photos/",  blank=True, null=True)
    birth_date = models.DateField("Дата рождения", blank=True, null=True)
    email = models.EmailField("Email", blank=True, null=True)
    phone_number = models.CharField("Номер телефона", max_length=11, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Category(models.Model):
    name = models.CharField("Название категории", max_length=255)

    class Meta:
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField("Название подкатегории", max_length=255)

    class Meta:
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    name = models.CharField("Название производителя", max_length=255)
    description = models.TextField("Описание производителя")

    class Meta:
        verbose_name_plural = "Производители"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField("Название товара", max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    article = models.CharField("Артикул товара", max_length=50, unique=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, verbose_name="Подкатегория")
    photo = models.FileField("Фото товара", upload_to="product_photos/")
    brand = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Бренд")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    description = models.TextField("Описание товара")
    video = models.FileField("Видеообзор товара", upload_to="videos/", blank=True, null=True)
    instruction = models.FileField("Инструкция по использованию", upload_to="product_instructions/", blank=True, null=True)
    quantity = models.PositiveIntegerField("Количество на складе")

    class Meta:
        verbose_name_plural = "Товары"

    def __str__(self):
        return f'{self.name}-{self.article}'

class Review(models.Model):
    subject = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField("Отзыв")
    stars = models.PositiveIntegerField("Оценка", default=5)
    
    class Meta:
        verbose_name_plural = "Отзывы"

class Favorite(models.Model):
    subject = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Избранное"

class NewsCategory(models.Model):
    type_choices = [
        ('Акции', 'Акции'),
        ('События', 'События'),
        ('Организация', 'Организация'),
    ]
    type = models.CharField("Тип новостей", choices=type_choices, max_length=20)

    class Meta:
        verbose_name_plural = "Категории новостей"
    
    def __str__(self):
        return self.type

class News(models.Model):
    name = models.CharField("Заголовок новости", max_length=255)
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE)
    photo = models.FileField("Изображение", upload_to="news/", blank=True, null=True)
    description = models.TextField("Описание новости")
    date = models.DateTimeField("Дата новости")

    class Meta:
        verbose_name_plural = "Новости"
    
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartProduct')
    
    class Meta:
        verbose_name_plural = "Корзина"

    def __str__(self):
        return f"Cart for {self.user_profile}"

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name_plural = "Компонент корзины"

    def __str__(self):
        return f"{self.quantity} шт x {self.product.name} в {self.cart}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с пользователем
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    delivery_address = models.CharField(max_length=255)
    comments = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    PAYMENT_CHOICES = [
        ('Наличными', 'Наличными'),
        ('Картой курьеру', 'Картой курьеру'),
    ]
    payment_choices = models.CharField("Форма оплаты", choices=PAYMENT_CHOICES, max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Заказ #{self.id} от {self.full_name}"

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name_plural = "Заказ"

    def __str__(self):
        return f"{self.quantity} шт x {self.product.name} в заказе {self.order}"

