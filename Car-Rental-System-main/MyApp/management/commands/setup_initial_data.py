import os
import shutil
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from MyApp.models import Car

class Command(BaseCommand):
    help = 'Seeds admin user and initial car catalog if empty'

    def handle(self, *args, **options):
        # Ensure media directory and car images exist
        media_car_dir = os.path.join(settings.MEDIA_ROOT, 'car', 'images')
        src_car_dir = os.path.join(settings.BASE_DIR, 'car', 'images')
        os.makedirs(media_car_dir, exist_ok=True)
        if os.path.exists(src_car_dir):
            for file in os.listdir(src_car_dir):
                dest_file = os.path.join(media_car_dir, file)
                if not os.path.exists(dest_file):
                    try:
                        shutil.copy2(os.path.join(src_car_dir, file), dest_file)
                    except Exception:
                        pass
        # 1. Create or update admin user
        admin_user, created = User.objects.get_or_create(username='admin')
        admin_user.password = 'admin123'
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.email = 'admin@example.com'
        admin_user.save()
        if created:
            self.stdout.write(self.style.SUCCESS("Admin user 'admin' created with password 'admin123'."))
        else:
            self.stdout.write(self.style.SUCCESS("Admin user 'admin' verified with password 'admin123'."))

        # 2. Seed default cars if table is empty
        if Car.objects.count() == 0:
            cars_data = [
                {'car_name': 'Renault', 'price': 1800, 'car_desc': 'Comfortable AC ;; Car Seating Capacity : 5 ;; Additional Features: Apple CarPlay', 'image': 'car/images/renault.jpg'},
                {'car_name': 'Alto 800', 'price': 700, 'car_desc': 'Comfortable AC Car :: Seating Capacity : 5 :: Additional Features: Voice Recognition', 'image': 'car/images/alto.webp'},
                {'car_name': 'Innova Crysta', 'price': 3500, 'car_desc': 'Comfortable AC Car :Seating Capacity : 7,8 :: Additional Features: Bluetooth Connect', 'image': 'car/images/innova.jpeg'},
                {'car_name': 'Chevy Traverse', 'price': 3000, 'car_desc': 'Comfortable AC Car : Seating Capacity : 8 :: Additional Features: Automatic Headlamps', 'image': 'car/images/taversa.jpg'},
                {'car_name': 'BMW X5', 'price': 10000, 'car_desc': 'Comfortable AC ;; Car Seating Capacity : 5 ;; Additional Features: Blind Spot detection', 'image': 'car/images/bmw.jpg'},
                {'car_name': 'Honda City', 'price': 2500, 'car_desc': 'Comfortable AC Car :: Seating Capacity : 5 Additional Features: High Speed Alert', 'image': 'car/images/honda.jpg'},
                {'car_name': 'Mercedes Benz', 'price': 40000, 'car_desc': 'Comfortable AC Car :: Seating Capacity : 5 :: Additional Features: Climate Control', 'image': 'car/images/mercedes.jpg'},
                {'car_name': 'Swift Dezire', 'price': 1000, 'car_desc': 'Comfortable AC Car :: Seating Capacity : 5 :: Additional Features: Alloy Wheels', 'image': 'car/images/swift.jpg'},
                {'car_name': 'KIA', 'price': 800, 'car_desc': 'Comfortable AC Car :: Seating Capacity : 5 :: Additional Features: Passenger Airbag', 'image': 'car/images/kia.webp'},
            ]
            for c in cars_data:
                car = Car(car_name=c['car_name'], price=c['price'], car_desc=c['car_desc'], image=c['image'])
                car.save()
            self.stdout.write(self.style.SUCCESS(f"Seeded {len(cars_data)} default cars into database."))
        else:
            self.stdout.write(f"Cars already exist ({Car.objects.count()} cars).")
