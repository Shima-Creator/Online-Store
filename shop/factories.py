import factory
from django.conf import settings
from django.contrib.auth.models import User
from shop.models import Product, SubCategory, Category, Salesman, Basket


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Sequence(lambda n: f'user{n}@example.com')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f'Category {n}')
    description = 'Test Category Description'


class SubCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubCategory

    name = factory.Sequence(lambda n: f'Subcategory {n}')
    description = 'Test Subcategory Description'
    category = factory.SubFactory(CategoryFactory)


class SalesmanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Salesman

    name = factory.Sequence(lambda n: f'Salesman {n}')


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f'Product {n}')
    photo = factory.django.ImageField(color='blue')  # Создаем фейковую картинку
    description = 'Some test description'
    price = 100.00
    subcategory = factory.SubFactory(SubCategoryFactory)
    shop = factory.SubFactory(SalesmanFactory)
    stock = 10


class BasketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Basket

    username = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 1