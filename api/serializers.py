from rest_framework import serializers
from django.core.exceptions import ValidationError
from geopy.distance import distance
from re import fullmatch
from .models import Location, Cargo, Truck


MAX_DISTANCE = 450


class LocationByZipcodeField(serializers.Field):
    def to_internal_value(self, data):
        if not fullmatch(r"\d{5}", data):
            message = 'This value does not match the required pattern.'
            raise ValidationError(message)

        location = None
        try:
            location = Location.objects.get(zipcode=data)
        except Location.DoesNotExist:
            message = 'Location with this zipcode does not exist.'
            raise ValidationError(message)
        return location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ['id']
        read_only = '__all__'


class CargoSerializer(serializers.ModelSerializer):
    pickup_location = LocationSerializer(read_only=True)
    delivery_location = LocationSerializer(read_only=True)
    pickup_zipcode = LocationByZipcodeField(source='pickup_location', write_only=True)
    delivery_zipcode = LocationByZipcodeField(source='delivery_location', write_only=True)

    class Meta:
        model = Cargo
        fields = (
            'id',
            'weight',
            'description',
            'pickup_location',
            'delivery_location',
            'pickup_zipcode',
            'delivery_zipcode',
        )


class CargoRetrieveSerializer(serializers.ModelSerializer):
    pickup_location = LocationSerializer(read_only=True)
    delivery_location = LocationSerializer(read_only=True)
    trucks = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.trucks_queryset = Truck.objects.select_related('location').only('number', 'location__lat', 'location__lng')
        super().__init__(*args, **kwargs)


    class Meta:
        model = Cargo
        fields = (
            'id',
            'weight',
            'description',
            'pickup_location',
            'delivery_location',
            'trucks',
        )

    def get_trucks(self, obj):
        if not hasattr(self, 'trucks_queryset'):
            self.trucks_queryset = Truck.objects.select_related('location').only('number', 'location__lat', 'location__lng')
        location = (obj.pickup_location.lat, obj.pickup_location.lng)
        serialized = TruckDistanceSerializer(instance=self.trucks_queryset, many=True, context={'location': location})
        return serialized.data


class CargoListSerializer(serializers.ModelSerializer):
    pickup_location = LocationSerializer()
    delivery_location = LocationSerializer()
    closest_trucks_count = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.trucks_queryset = Truck.objects.select_related('location').values('location__lat', 'location__lng')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Cargo
        fields = (
            'id',
            'weight',
            'description',
            'pickup_location',
            'delivery_location',
            'closest_trucks_count',
        )

    def get_closest_trucks_count(self, obj):
        pickup_location = (obj.pickup_location.lat, obj.pickup_location.lng)

        closest_trucks_count = \
            sum(1 for truck in self.trucks_queryset if
                distance(pickup_location, (truck['location__lat'], truck['location__lng'])).miles <= MAX_DISTANCE)
                # distance(pickup_location, (truck.location.lat, truck.location.lng)).miles <= MAX_DISTANCE)

        return closest_trucks_count


class TruckDistanceSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Truck
        fields = ('id', 'number', 'distance',)

    def get_distance(self, obj):
        return distance((obj.location.lat, obj.location.lng), self.context.get("location")).miles


class TruckSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    zipcode = LocationByZipcodeField(source='location', write_only=True)

    class Meta:
        model = Truck
        fields = (
            'id',
            'number',
            'load_capacity',
            'zipcode',
            'location',
        )
