from cargo.celery import app
from .models import Truck, Location
import random


location_ids = Location.objects.values_list("id", flat=True)

@app.task
def update_all_truck_locations_randomly():
    trucks = Truck.objects.only('id').all()
    for truck in trucks:
        truck.location_id = random.choice(location_ids)
    Truck.objects.bulk_update(trucks, ["location_id"])


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(15, update_all_truck_locations_randomly)
