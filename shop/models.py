from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from users.models import Seller


#The abstract model
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        # Установить время удаления вместо удаления строки
        self.deleted_at = now()
        self.save()

    def hard_delete(self, using=None, keep_parents=False):
        # Реальное удаление строки, если необходимо
        super().delete(using, keep_parents)

    def restore(self):
        # Восстановление "удаленной" строки
        self.deleted_at = None
        self.save()

    @property
    def is_deleted(self):
        return self.deleted_at is not None


#The model with categories of products
class Category(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Имя категории')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = "Категории"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name


#The model with subcategories of products
class SubCategory(BaseModel):
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='Имя подкатегории')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = "Подкатегории"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return f"{self.category} - {self.name}"


#The model with products
class Product(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Товар')
    photo = models.ImageField(upload_to='product', default='Add you photo...', verbose_name='Фото')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    subcategory = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE, verbose_name='Подкатегория')
    shop = models.ForeignKey('Shop', related_name='shops', on_delete=models.CASCADE, verbose_name='Магазин')
    stock = models.PositiveIntegerField(verbose_name='В наличии')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


#The model with salesmans
class Shop(models.Model):
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE, related_name='shop')
    shop_name = models.CharField(max_length=100, verbose_name='Продавец')
    country = models.CharField(max_length=40, verbose_name='Страна')
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'

    def __str__(self):
        return self.shop_name


#The model of basket for products
class Basket(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', unique=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товары')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

    def __str__(self):
        return f"{self.username} products: {self.product}"

    @property
    def total_price_for_product(self):
        return self.product.price * self.quantity

    @property
    def total_price_for_all(self):
        total_price = 0
        for product in Basket.objects.all():
            total_price += (product.quantity * product.product.price)

        return total_price


class ProductStatus(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', unique=False)
    product = models.OneToOneField(Product, related_name='product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    paid = models.BooleanField(default=False, verbose_name='Оплачен')
    in_delivery = models.BooleanField(default=False, verbose_name='Доставляется')
    delivered_in_shop = models.BooleanField(default=False, verbose_name='Прибыл в ПВЗ')
    received_by_the_buyer = models.BooleanField(default=False, verbose_name='Получен покупателем')
    returned = models.BooleanField(default=False, verbose_name='Возвращен')
