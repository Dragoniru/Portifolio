from django.test import TestCase
from .views import calculate_fastest_route, get_and_display_json

class RouteCalculationTests(TestCase):
    def test_calculate_fastest_route(self):
        # JSON
        url = "https://mocki.io/v1/10404696-fd43-4481-a7ed-f9369073252f"

        fetched_json = get_and_display_json(url)

        if not fetched_json:
            self.fail("Falha ao recuperar dados JSON")

        start_point = "A5"
        pickup_point = "E3"
        delivery_point = "G1"

        expected_route = ['A5', 'A4', 'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'F2', 'E2', 'D2', 'C2', 'B2', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1']
        expected_time = 281.69

        route, time = calculate_fastest_route(start_point, pickup_point, delivery_point, fetched_json)

        self.assertEqual(route, expected_route)
        self.assertEqual(time, expected_time)
