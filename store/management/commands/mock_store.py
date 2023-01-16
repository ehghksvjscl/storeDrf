from django.core.management.base import BaseCommand, no_translations
from store.models import Product, Option
class Command(BaseCommand):

    help = "This command creates products and options"
    
    @no_translations
    def handle(self, *args, **options):
        Product.objects.all().delete()
        Option.objects.all().delete()
        products = [
            {
                "name": "위처3",
                "price": 1000000,
                "options": [
                    {
                        "name": "기본",
                        "price": 0,
                        "stock": 10,
                    },
                    {
                        "name": "DLC 하츠 오브 스톤",
                        "price": 1100000,
                        "stock": 10,
                    },
                    {
                        "name": "DLC 블러드 앤 와인",
                        "price": 1200000,
                        "stock": 10,
                    },
                ],
            },
            {
                "name": "WOW",
                "price": 1200000,
                "options": [
                    {
                        "name": "DLC 리치 왕의 분노",
                        "price": 1200000,
                        "stock": 10,
                    },
                    {
                        "name": "DLC 불타는 성전",
                        "price": 1300000,
                        "stock": 10,
                    },
                    {
                        "name": "DLC 군단",
                        "price": 1400000,
                        "stock": 10,
                    },
                ],
            },
            {
                "name": "스플렌더",
                "price": 1400000,
                "options": [
                    {
                        "name": "대도시",
                        "price": 1400000,
                        "stock": 10,
                    },
                    {
                        "name": "교역로",
                        "price": 1500000,
                        "stock": 10,
                    },
                    {
                        "name": "동방무역",
                        "price": 1600000,
                        "stock": 10,
                    },
                ],
            },
        ]
        for product in products:
            p = Product.objects.create(name=product["name"], price=product["price"])
            for option in product["options"]:
                Option.objects.create(
                    product=p,
                    name=option["name"],
                    price=option["price"],
                    stock=option["stock"],
                )

        self.stdout.write(self.style.SUCCESS("Mock data created!"))

