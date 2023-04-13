import itertools
from typing import Optional

from django.contrib.gis.db.models.functions import Distance as D
from django.contrib.gis.geos import Point
from geopy.distance import distance

from ..models import Vehicle, Swap
from ..shift.path import calculate_order


class ShiftDependencies:
    LIMIT = 20

    def __init__(self, point: Point, shift_id: int):
        self.point = point
        self.shift_id = shift_id
        self.vehicles: Optional[list[Vehicle]] = None
        self.graph: Optional[list[list[float]]] = None

    def __find_closest(self) -> list[Vehicle]:
        """ Find the closest vehicles to the point """
        return list(Vehicle.objects.annotate(
            distance=D('location', self.point)
        ).order_by('distance')[:self.LIMIT])

    def __build_graph(self) -> list[list[float]]:
        """ Build a graph of vehicles/distances """
        self.vehicles = [Vehicle(location=self.point), *self.__find_closest()]
        n = len(self.vehicles)

        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                graph[i][j] = distance(self.vehicles[i].location, self.vehicles[j].location).miles

        return graph

    def build(self) -> None:
        """ Create Swaps and build optimal order of Vehicles to visit """
        graph = self.__build_graph()

        indexes = calculate_order(graph)

        Swap.objects.bulk_create(
            [Swap(shift_id=self.shift_id, vehicle_id=self.vehicles[index].id) for index in itertools.islice(indexes, 1, len(self.vehicles))],
            ignore_conflicts=True,
        )
