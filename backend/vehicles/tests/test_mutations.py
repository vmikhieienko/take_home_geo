import json

from graphene_django.utils.testing import GraphQLTestCase
from ..models import Shift, Swap, Vehicle


class TestCreateShiftManualMutation(GraphQLTestCase):
    def setUp(self) -> None:
        response = self.query(
            '''
            mutation createShiftManual {
                createShiftManual {
                    shift {
                        id,
                    }
                }
            }
            '''
        )
        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        self.shift = content.get('data', {}).get('createShiftManual', {}).get('shift', {})

    def test_mutation(self):
        self.assertIn('id', self.shift)


class TestAddVehiclesToShiftMutation(GraphQLTestCase):
    @classmethod
    def setUpTestData(cls):
        Shift.objects.create(id=1)

    def setUp(self) -> None:
        response = self.query(
            '''
            mutation addVehiclesToShift ($shift_id: ID!, $vehicle_ids: [ID]!) {
                addVehiclesToShift (args: {shiftId: $shift_id, vehicleIds: $vehicle_ids}) {
                    shift {
                        id,
                        vehicles {
                            id,
                        }
                    }
                }
            }
            ''', variables={'shift_id': 1, 'vehicle_ids': [3, 4]}
        )
        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        self.shift = content.get('data', {}).get('addVehiclesToShift', {}).get('shift', {})

    def test_mutation(self):
        expected = {
            'id': '1',
            'vehicles': [
                {
                    'id': '3',
                },
                {
                    'id': '4',
                },
            ],
        }
        self.assertDictEqual(self.shift, expected)


class TestCompleteSwapMutation(GraphQLTestCase):
    @classmethod
    def setUpTestData(cls):
        shift, vehicle = Shift.objects.create(id=1), Vehicle.objects.get(id=1)
        Swap.objects.create(id=1, shift=shift, vehicle=vehicle, completed=False)

    def setUp(self):
        response = self.query(
            '''
            mutation completeSwap ($shift_id: ID!, $vehicle_id: ID!) {
                completeSwap (args: {shiftId: $shift_id, vehicleId: $vehicle_id} ) {
                    swap {
                        id,
                        completed
                        vehicle {
                            id,
                            batteryLevel,
                        }
                    }
                }
            }
            ''', variables={'shift_id': 1, 'vehicle_id': 1}
        )
        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        self.swap = content.get('data', {}).get('completeSwap', {}).get('swap', {})

    def test_mutation(self):
        expected = {
            'id': '1',
            'completed': True,
            'vehicle': {
                'id': '1',
                'batteryLevel': 100
            }
        }
        self.assertDictEqual(self.swap, expected)


class TestTestCreateShiftAutoMutation(GraphQLTestCase):
    def setUp(self) -> None:
        response = self.query(
            '''
            mutation createShiftAuto($lat: Float!, $lon: Float!) {
              createShiftAuto (args: {lat: $lat, lon: $lon}) {
                shift {
                  id
                  vehicles {
                    id
                    batteryLevel
                    location {
                      type
                      coordinates
                    }
                  }
                }
              }
            }
            ''', variables={'lat': 40.679135, 'lon': -73.897627}
        )

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        self.shift = content.get('data', {}).get('createShiftAuto', {}).get('shift', {})

    def test_shift_created(self):
        self.assertIn('id', self.shift)

    def test_shift_vehicles_order(self):
        vehicle_ids = [vehicle['id'] for vehicle in self.shift.get('vehicles', [])]
        expected = ['12', '11', '10', '4', '15', '5', '6', '8', '1', '3', '2', '9', '7', '14', '13']
        self.assertListEqual(vehicle_ids, expected)
