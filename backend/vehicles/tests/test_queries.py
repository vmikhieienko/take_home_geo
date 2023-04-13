import json

from graphene_django.utils.testing import GraphQLTestCase

from ..models import Shift, Swap, Vehicle

class TestAllShiftsQuery(GraphQLTestCase):
    @classmethod
    def setUpTestData(cls):
        Shift.objects.create(id=1)

    def setUp(self) -> None:
        response = self.query(
            '''
            query allShifts {
                allShifts {
                    id,
                }
            }
            '''
        )
        self.assertResponseNoErrors(response)

        self.content = json.loads(response.content)

    def test_query(self):
        expected = {
            'data': {
                'allShifts': [
                    {
                        'id': '1'
                    },
                ],
            }
        }
        self.assertDictEqual(self.content, expected)


class TestAllVehiclesQuery(GraphQLTestCase):
    def setUp(self) -> None:
        response = self.query(
            '''
            query allVehicles {
                allVehicles {
                    id,
                    licensePlate,
                    batteryLevel,
                    model,
                    inUse,
                    location {
                        coordinates,
                    },
                }
            }
            '''
        )
        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        self.vehicles = content.get('data', {}).get('allVehicles', [{}])

    def test_vehicle_amount(self):
        self.assertEqual(len(self.vehicles), 15)

    def test_first_vehicle(self):
        expected = {
            'id': '1',
            'licensePlate': 'NY0001',
            'batteryLevel': 90,
            'model': 'Niu',
            'inUse': True,
            'location': {
                'coordinates': [40.680245, -73.996955],
            }
        }
        self.assertDictEqual(self.vehicles[0], expected)


class TestSwapQuery(GraphQLTestCase):
    @classmethod
    def setUpTestData(cls):
        shift, vehicle = Shift.objects.create(id=1), Vehicle.objects.get(id=1)
        Swap.objects.create(id=1, shift=shift, vehicle=vehicle)

    def setUp(self) -> None:
        response = self.query(
            '''
            query swap ($shift_id: ID!, $vehicle_id: ID!) {
                swap (shiftId: $shift_id, vehicleId: $vehicle_id){
                    id,
                    completed,
                    vehicle {
                        id,
                        licensePlate,
                    },
                }
            }
            ''', variables={'shift_id': 1, 'vehicle_id': 1}
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.swap = content.get('data', {}).get('swap', {})

    def test_query(self):
        expected = {
            'id': '1',
            'completed': False,
            'vehicle': {
                'id': '1',
                'licensePlate': 'NY0001'
            }
        }
        self.assertDictEqual(self.swap, expected)


class TestShiftQuery(GraphQLTestCase):
    @classmethod
    def setUpTestData(cls):
        shift, vehicle = Shift.objects.create(id=1), Vehicle.objects.get(id=1)
        Swap.objects.create(id=1, shift=shift, vehicle=vehicle)

    def setUp(self) -> None:
        response = self.query(
            '''
            query shift ($shift_id: ID!) {
                shift (shiftId: $shift_id){
                    id,
                    swaps {
                        id,
                        completed,
                        vehicle {
                            id,
                            licensePlate,
                        },
                    }
                    vehicles {
                        id,
                        licensePlate,
                        batteryLevel,
                    }
                }
            }
            ''', variables={'shift_id': 1}
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.shift = content.get('data', {}).get('shift', {})

    def test_shift_swaps(self):
        swaps = self.shift.get('swaps', [{}])
        expected = [{'id': '1', 'completed': False, 'vehicle': {'id': '1', 'licensePlate': 'NY0001'}}]

        self.assertListEqual(swaps, expected)

    def test_shift_vehicles(self):
        vehicles = self.shift.get('vehicles', [{}])
        expected = [{'id': '1', 'licensePlate': 'NY0001', 'batteryLevel': 90}]

        self.assertListEqual(vehicles, expected)
