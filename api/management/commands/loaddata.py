from django.core.management.base import BaseCommand
from api.models import Location, Truck, Cargo
import csv
import random


class Command(BaseCommand):
    help = 'Loading initial data into the DB.'

    def handle(self, *args, **kwargs):
        if Location.objects.exists():
            self.stdout.write(self.style.SUCCESS('DB not empty.'))
        else:
            create_locations('api/fixtures/zips.csv')
            location_ids = Location.objects.values_list("id", flat=True)
            create_trucks('api/fixtures/trucks.csv', location_ids)
            create_cargos(location_ids, 10)
            self.stdout.write(self.style.SUCCESS('Initial DB data loaded.'))


def create_locations(filepath):
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)

        Location.objects.bulk_create(
            Location(
                zipcode=row[0],
                lat=row[1],
                lng=row[2],
                city=row[3],
                state_name=row[5],
            ) for row in reader
        )


def create_trucks(filepath, location_ids):
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)

        Truck.objects.bulk_create(
            Truck(
                location_id=random.choice(location_ids),
                number=row[0],
                load_capacity=int(row[1]),
            ) for row in reader
        )


def create_cargos(location_ids, quantity):
    Cargo.objects.bulk_create(
        Cargo(
            pickup_location_id=random.choice(location_ids),
            delivery_location_id=random.choice(location_ids),
            weight=random.randint(1, 10000),
            description='Sample description.'
        ) for _ in range(quantity)
    )
