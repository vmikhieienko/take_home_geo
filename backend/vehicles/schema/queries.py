from typing import Iterable

import graphene as gql

from ..models import Swap, Vehicle, Shift
from .types import ListShiftType, VehicleType, SingleShiftType, SwapType


class Query(gql.ObjectType):
    all_shifts = gql.List(
        ListShiftType,
        description='Show all Shifts'
    )
    all_vehicles = gql.List(
        VehicleType,
        description='Show all Vehicles'
    )
    shift = gql.Field(
        SingleShiftType,
        shift_id=gql.ID(),
        description='Show a Shift with attached Vehicles and Swaps'
    )
    swap = gql.Field(
        SwapType,
        shift_id=gql.ID(),
        vehicle_id=gql.ID(),
        description='Show a Swap with attached Vehicle'
    )

    def resolve_swap(self, info, shift_id, vehicle_id) -> Swap:
        return Swap.objects.get(shift_id=shift_id, vehicle_id=vehicle_id)

    def resolve_all_vehicles(self, info) -> Iterable[Vehicle]:
        return Vehicle.objects.all()

    def resolve_all_shifts(self, info) -> Iterable[Shift]:
        return Shift.objects.all()

    def resolve_shift(self, info, shift_id) -> Shift:
        return Shift.objects.get(pk=shift_id)
