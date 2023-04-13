from django.test import TestCase
from ..shift.path import calculate_order


class TestShiftPath(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.graph = [
            [0, 10, 18, 40, 20],
            [10, 0, 35, 15, 12],
            [18, 35, 0, 25, 25],
            [40, 15, 25, 0, 30],
            [20, 13, 25, 30, 0],
        ]

    def test_path_creation(self):
        result = calculate_order(self.graph)

        self.assertListEqual(result, [0, 1, 3, 4, 2])
