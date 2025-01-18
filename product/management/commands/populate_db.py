import os
import random
import json

from django.core.management.base import BaseCommand

from order.models import Order, OrderItem
from product.models import Product
from user.models import User


class Command(BaseCommand):
    help = 'Creates application data'

    def handle(self, *args, **kwargs):
        # Get or create users
        users_data = [
            {"username": "manager", "password": "manager", "is_superuser": True, "is_staff": True},
            {"username": "vendor", "password": "vendor", "is_superuser": False, "is_staff": True},
        ]

        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data["username"],
                defaults={
                    "is_superuser": user_data["is_superuser"],
                    "is_staff": user_data["is_staff"]
                }
            )
            if created:
                user.set_password(user_data["password"])  # Hash the password
                user.save()
                self.stdout.write(self.style.SUCCESS(f'User "{user.username}" has been created.'))
            else:
                self.stdout.write(self.style.WARNING(f'User "{user.username}" already exists.'))


        # Removal existing products and orders
        Product.objects.all().delete()
        Order.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Products and orders have been removed.'))

        # Load product data from JSON file
        current_directory = os.path.dirname(os.path.abspath(__file__))  # Chemin absolu du script
        file_path = os.path.join(current_directory, 'products_list.json')

        try:
            with open(file_path, 'r') as file:
                products_list = json.load(file)
            self.stdout.write(self.style.SUCCESS('Product data has been loaded from JSON file.'))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR('Error: products_list.json file not found.'))
            return
        except json.JSONDecodeError as e:
            self.stderr.write(self.style.ERROR(f'Error: Failed to decode JSON file. {e}'))
            return

        # Create products
        products = [Product(**product) for product in products_list]
        Product.objects.bulk_create(products)
        self.stdout.write(self.style.SUCCESS('Products are created.'))

        # Create some dummy orders tied to Manager & Vendor
        users = [
            {"user": User.objects.filter(username="manager").first(), "name": "manager"},
            {"user": User.objects.filter(username="vendor").first(), "name": "vendor"},
        ]

        for user_data in users:
            user = user_data["user"]

            if not user:
                self.stderr.write(self.style.ERROR(f'Error: {user} user not found.'))
                continue

            # Créer des commandes fictives pour l'utilisateur
            for _ in range(5):  # Ajuste le nombre de commandes ici
                order = Order.objects.create(user=user)
                for product in random.sample(list(Product.objects.all()), 4):
                    OrderItem.objects.create(
                        order=order, product=product, quantity=random.randint(1, 5)
                    )

            self.stdout.write(self.style.SUCCESS(f'Dummy orders for {user} created.'))

        self.stdout.write(self.style.SUCCESS('Dummy orders for manager and vendor created.'))
        self.stdout.write(self.style.SUCCESS('Your project is ready !'))
