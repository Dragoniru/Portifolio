import requests
from django.shortcuts import render
from django.contrib import messages
from .models import Route

url = "https://mocki.io/v1/10404696-fd43-4481-a7ed-f9369073252f"

def get_and_display_json(url_loc):
    try:
        response = requests.get(url_loc)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao acessar a URL: {e}")
        return None

def find_next_move(current_pos, visited, json_data):
    next_moves = json_data.get(current_pos, {})
    quickest_move = float('inf')
    quickest_move_pos = None

    for pos, mov_time in next_moves.items():
        if pos not in visited and mov_time < quickest_move:
            quickest_move = mov_time
            quickest_move_pos = pos

    return quickest_move_pos


def calculate_subroute(start, end, json_data):
    visited = None
    route = [start]
    visited = set(route)

    while route[-1] != end:
        next_move = find_next_move(route[-1], visited, json_data)
        if next_move is None:
            return None  # Rota não encontrada
        route.append(next_move)
        visited.add(next_move)

    return route


def calculate_fastest_route(start, pickup, delivery, json_data):
    route_to_pickup = calculate_subroute(start, pickup, json_data)
    if route_to_pickup is None:
        return None, 0

    route_to_delivery = calculate_subroute(pickup, delivery, json_data)
    if route_to_delivery is None:
        return None, 0

    full_route = route_to_pickup + route_to_delivery[1:]
    total_time = sum(json_data[full_route[i]][full_route[i + 1]] for i in range(len(full_route) - 1))

    return full_route, total_time


def index(request):
    chessboard_positions = [f"{chr(letter)}{number}" for letter in range(ord('A'), ord('H') + 1) for number in
                            range(1, 9)]

    if request.method == 'POST':
        start = request.POST.get('route_start')
        pickup = request.POST.get('pickup_point')
        delivery = request.POST.get('delivery')

        if not all([start, pickup, delivery]):
            messages.error(request, "Todos os campos devem ser preenchidos.")
        elif start == pickup or pickup == delivery or start == delivery:
            messages.error(request, "Os pontos de partida, coleta e entrega devem ser diferentes.")
        else:
            json_data = get_and_display_json(url)
            if json_data:
                route, time_taken = calculate_fastest_route(start, pickup, delivery, json_data)
                if route:
                    Route.objects.create(start=start, pickup=pickup, delivery=delivery)
                    messages.success(request, f"Rota calculada: {' -> '.join(route)}. Tempo: {time_taken} segundos.")
                else:
                    messages.error(request, "Não foi possível criar uma rota.")

    route_history = Route.objects.all().order_by('-date')[:10]
    context = {
        'route_history': route_history,
        'chessboard_positions': chessboard_positions,
    }
    return render(request, 'index.html', context)
