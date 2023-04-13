import graphql_geojson

from graphene import List
from graphene_django import DjangoObjectType, DjangoListField

from ..models import Swap, Vehicle, Shift


class SwapType(DjangoObjectType):
    class Meta:
        model = Swap
        fields = '__all__'


class VehicleType(DjangoObjectType):
    class Meta:
        model = Vehicle
        fields = '__all__'
        geojson_field = 'location'


class ListShiftType(DjangoObjectType):
    class Meta:
        model = Shift
        fields = '__all__'

    swaps = DjangoListField(SwapType)


class SingleShiftType(DjangoObjectType):
    class Meta:
        model = Shift
        fields = '__all__'

    swaps = DjangoListField(SwapType)
    vehicles = List(VehicleType)

    @staticmethod
    def resolve_vehicles(parent, info):
        return Vehicle.objects.filter(swaps__shift=parent).order_by('swaps__id')
