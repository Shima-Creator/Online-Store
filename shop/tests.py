from django.test import TestCase
from django.db import IntegrityError

from shop.factories import *
from decimal import Decimal


class CategoryModelTests(TestCase):
    def test_create_category(self):
        """Тестирование создания экземпляра Category"""
        category = Category.objects.create(name='Test Category', description='Test Category Description')
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.description, 'Test Category Description')

    def test_category_str_method(self):
        """Тестирование метода __str__ модели Category"""
        category = CategoryFactory(name='Test Category Name')
        self.assertEqual(str(category), 'Test Category Name')

class SubCategoryModelTests(TestCase):
    def test_create_subcategory(self):
        """Тестирование создания экземпляра SubCategory"""
        category = CategoryFactory()
        subcategory = SubCategory.objects.create(
            name='Test Subcategory',
            description='Test Subcategory Description',
            category=category
        )
        self.assertEqual(SubCategory.objects.count(), 1)
        self.assertEqual(subcategory.name, 'Test Subcategory')
        self.assertEqual(subcategory.description, 'Test Subcategory Description')
        self.assertEqual(subcategory.category, category)

    def test_subcategory_str_method(self):
        """Тестирование метода __str__ модели SubCategory"""
        subcategory = SubCategoryFactory(name='Test SubCategory Name')
        self.assertEqual(str(subcategory), 'Test SubCategory Name')

    def test_subcategory_relationship(self):
        """Тестирование связи подкатегории с категорией"""
        category = CategoryFactory()
        subcategory = SubCategoryFactory(category = category)

        self.assertEqual(subcategory.category, category)
        self.assertIn(subcategory, category.category.all())

class ProductModelTests(TestCase):
    def test_create_product(self):
        """Тестирование создания экземпляра Product"""
        subcategory = SubCategoryFactory()
        salesman = SalesmanFactory()
        product = Product.objects.create(
            name='Test Product',
            description='Test description',
            price=Decimal('99.99'),
            subcategory=subcategory,
            shop=salesman,
            stock=50
        )

        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.description, 'Test description')
        self.assertEqual(product.price, Decimal('99.99'))
        self.assertEqual(product.subcategory, subcategory)
        self.assertEqual(product.shop, salesman)
        self.assertEqual(product.stock, 50)

    def test_create_product_with_factory(self):
         """Тестирование создания экземпляра Product с помощью фабрики"""
         product = ProductFactory()
         self.assertTrue(isinstance(product, Product))
         self.assertIsNotNone(product.name)
         self.assertIsNotNone(product.photo)
         self.assertIsNotNone(product.description)
         self.assertIsNotNone(product.price)
         self.assertIsNotNone(product.subcategory)
         self.assertIsNotNone(product.shop)
         self.assertIsNotNone(product.stock)

    def test_product_name_max_length(self):
         """Тестирование ограничения максимальной длины поля name"""
         with self.assertRaises(IntegrityError):
            Product.objects.create(
                name='a' * 256,
                description='Test description',
                price=Decimal('99.99'),
                subcategory=SubCategoryFactory(),
                shop=SalesmanFactory(),
                stock=10
            )

    def test_product_price_decimal_places(self):
         """Тестирование ограничения decimal_places для цены"""
         subcategory = SubCategoryFactory()
         salesman = SalesmanFactory()
         product = Product.objects.create(
            name='Test Product',
            description='Test description',
            price=Decimal('99.99'),
            subcategory=subcategory,
            shop=salesman,
            stock=50
         )
         self.assertEqual(product.price, Decimal('99.99'))

    def test_product_stock_is_positive(self):
        """Тестирование ограничения на положительность значения в стоке"""
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                name="Test Product",
                description="Test description",
                price=Decimal('99.99'),
                subcategory=SubCategoryFactory(),
                shop=SalesmanFactory(),
                stock=-10
            )

    def test_product_str_method(self):
        """Тестирование метода __str__ модели Product"""
        product = ProductFactory(name='Test Product Name')
        self.assertEqual(str(product), 'Test Product Name')

    def test_product_image_default(self):
        """Тестирование дефолтного значения для картинки"""
        product = ProductFactory(photo = 'Add you photo...')
        self.assertEqual(product.photo, 'Add you photo...')

    def test_product_relationship(self):
        """Тестирование связи с подкатегорией и магазином"""
        subcategory = SubCategoryFactory()
        salesman = SalesmanFactory()
        product = ProductFactory(subcategory=subcategory, shop=salesman)

        self.assertEqual(product.subcategory, subcategory)
        self.assertEqual(product.shop, salesman)
        self.assertIn(product, subcategory.products.all())
        self.assertIn(product, salesman.shops.all())

class BasketModelTests(TestCase):
    def test_create_basket_item(self):
        """Тестирование создания элемента корзины"""
        user = UserFactory()
        product = ProductFactory()
        basket_item = Basket.objects.create(username = user, product=product, quantity=2)

        self.assertEqual(Basket.objects.count(), 1)
        self.assertEqual(basket_item.username, user)
        self.assertEqual(basket_item.product, product)
        self.assertEqual(basket_item.quantity, 2)

    def test_basket_item_default_quantity(self):
        """Тестирование дефолтного количества в корзине"""
        user = UserFactory()
        product = ProductFactory()
        basket_item = Basket.objects.create(username = user, product=product)
        self.assertEqual(basket_item.quantity, 1)

    def test_basket_item_with_factory(self):
        """Тестирование создания элемента корзины с помощью фабрики"""
        basket_item = BasketFactory()
        self.assertTrue(isinstance(basket_item, Basket))
        self.assertIsNotNone(basket_item.username)
        self.assertIsNotNone(basket_item.product)
        self.assertIsNotNone(basket_item.quantity)

    def test_basket_item_relationship(self):
        """Тестирование связи элемента корзины с пользователем и продуктом"""
        user = UserFactory()
        product = ProductFactory()
        basket_item = BasketFactory(username = user, product=product)
        self.assertEqual(basket_item.username, user)
        self.assertEqual(basket_item.product, product)

