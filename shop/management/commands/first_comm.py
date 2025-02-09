import os
from email.policy import default
from tkinter.font import names

from django.core.files.base import ContentFile, File
from django_seed import Seed
from faker import Faker
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand


from shop.models import Category, SubCategory, Product, Salesman


class Command(BaseCommand):
    help = "The first command for management"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            help='Number of records to create',
            default=2
        )

        parser.add_argument(
            '--delete',
            action='store_true',
            help='Set this flat to true'
        )

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        delete = kwargs['delete']

        if delete:
            Category.objects.all().delete()
            SubCategory.objects.all().delete()
            Product.objects.all().delete()

            path = settings.MEDIA_ROOT / 'product'

            for file in os.listdir(path):
                os.remove(os.path.join(path, file))

            print('Flushed models')
            return

        settings.USE_TZ = False
        print('Seed data by Seeder')
        seeder = Seed.seeder()

        print('Seeding categories')
        seeder.add_entity(Category, count, {
            'name': lambda x: seeder.faker.sentence(),
            'description': lambda x: seeder.faker.text(),
            'deleted_at': None
        })

        print('Seeding subcategories')
        seeder.add_entity(SubCategory, count, {
            'category': lambda x: Category.objects.order_by('?').first(),
            'name': lambda x: seeder.faker.sentence(),
            'description': lambda x: seeder.faker.text(),
            'deleted_at': None
        })

        file_name = seeder.faker.file_name(extension='jpeg')
        print('Seeding products')
        seeder.add_entity(Product, count, {
            'name': lambda x: seeder.faker.sentence(),
            'description': lambda x: seeder.faker.text(),
            'photo': lambda x: File(ContentFile(seeder.faker.text(),file_name)
            ),
            'price': lambda x: seeder.faker.random_number(),
            'subcategory': lambda x: SubCategory.objects.order_by('?').first(),
            'shop': lambda x: Salesman.objects.order_by('?').first(),
            'stock':lambda x: seeder.faker.random_number(),
            'deleted_at': None
        })

        seeder.execute()

        ########################################################

        fake = Faker('ru_RU')

        for _ in range(count):
            print('Seeding categories')
            Category.objects.create(
                name=fake.sentence(),
                description=fake.text(),
                created_at=fake.date_time_this_year(before_now=True, after_now=False),
                updated_at=fake.date_time_this_year(before_now=True, after_now=False)
            )

            print('Seeding subcategories')
            SubCategory.objects.create(
                category=Category.objects.order_by('?').first(),
                name=fake.sentence(),
                description=fake.text(),
                created_at=fake.date_time_this_year(before_now=True, after_now=False),
                updated_at=fake.date_time_this_year(before_now=True, after_now=False)
            )

            file_name = fake.file_name(extension='jpeg')
            file_content = fake.text()

            content_file = ContentFile(file_content, file_name)

            print('Seeding products')
            Product.objects.create(
                name=fake.sentence(),
                description=fake.text(),
                photo=content_file,
                price=fake.random_number(),
                shop=Salesman.objects.order_by('?').first(),
                subcategory=SubCategory.objects.order_by('?').first,
                stock=fake.random_number(),
                created_at = fake.date_time_this_year(before_now=True, after_now=False),
                updated_at = fake.date_time_this_year(before_now=True, after_now=False)
            )

        settings.USE_TZ = True