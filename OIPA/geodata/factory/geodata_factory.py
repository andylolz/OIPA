from django.contrib.gis.geos import Point
import factory
from geodata import models


class NoDatabaseFactory(factory.django.DjangoModelFactory):
    @classmethod
    def _setup_next_sequence(cls):
        return 0


class CityFactory(NoDatabaseFactory):
    class Meta:
        model = models.City

    geoname_id = 1000
    name = 'dummy_city'
    location = Point(5, 23)


class CountryFactory(NoDatabaseFactory):
    class Meta:
        model = models.Country

    code = 'OO'
    name = 'dummy_country'
    center_longlat = Point(1, 3)
