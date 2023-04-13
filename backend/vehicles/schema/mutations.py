import graphene as gql
from django.contrib.gis.geos import Point

from django.db import transaction

from ..models import Shift, Swap
from .types import SingleShiftType, SwapType
from ..shift.dependencies import ShiftDependencies


class CreateShiftManual(gql.Mutation):
    shift = gql.Field(SingleShiftType, required=True)

    @staticmethod
    def mutate(root, info):
        shift_instance = Shift()
        shift_instance.save()
        return CreateShiftManual(shift=shift_instance)


class AddVehiclesToShiftInput(gql.InputObjectType):
    shift_id = gql.ID()
    vehicle_ids = gql.List(gql.ID)


class AddVehiclesToShift(gql.Mutation):
    class Arguments:
        args = AddVehiclesToShiftInput(required=True)

    shift = gql.Field(SingleShiftType, required=True)

    @staticmethod
    def mutate(root, info, args):
        shift = Shift.objects.get(id=args.shift_id)

        shift.swaps.bulk_create([Swap(
            vehicle_id=vehicle_id,
            shift_id=args.shift_id,
        ) for vehicle_id in args.vehicle_ids], ignore_conflicts=True)

        return AddVehiclesToShift(shift=shift)


class CompleteSwapInput(gql.InputObjectType):
    shift_id = gql.ID()
    vehicle_id = gql.ID()


class CompleteSwap(gql.Mutation):
    class Arguments:
        args = CompleteSwapInput(required=True)

    swap = gql.Field(SwapType, required=True)

    @staticmethod
    @transaction.atomic
    def mutate(root, info, args):
        swap = Swap.objects.get(shift_id=args.shift_id, vehicle_id=args.vehicle_id)

        swap.vehicle.battery_level = 100
        swap.vehicle.save()

        swap.completed = True
        swap.save()

        return CompleteSwap(swap=swap)


class CreateShiftAutoInput(gql.InputObjectType):
    lat = gql.Float()
    lon = gql.Float()


class CreateShiftAuto(gql.Mutation):
    class Arguments:
        args = CreateShiftAutoInput(required=True)

    shift = gql.Field(SingleShiftType, required=True)

    @staticmethod
    @transaction.atomic
    def mutate(root, info, args):
        point = Point(args.lat, args.lon, srid=4326)
        shift_instance = Shift()
        shift_instance.save()

        ShiftDependencies(point, shift_instance.id).build()

        return CreateShiftAuto(shift=shift_instance)


class Mutation(gql.ObjectType):
    create_shift_auto = CreateShiftAuto.Field(description='Create Shift Automatically')
    create_shift_manual = CreateShiftManual.Field(description='Create empty Shift')
    add_vehicles_to_shift = AddVehiclesToShift.Field(description='Add Vehicles to Shift')
    complete_swap = CompleteSwap.Field(description='Complete Swap for Vehicle in a Shift')
