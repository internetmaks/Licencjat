from typing import List, Dict, Set

def route_is_valid(route: List[int], allowed: Dict[int, Set[int]], num_cities: int):
    if len(route) != num_cities:
        return False
    if len(set(route)) != num_cities:
        return False
    if any(i < 0 or i >= num_cities for i in route):
        return False
    for pos, city in enumerate(route):
        if pos not in allowed.get(city, set()):
            return False
    return True

def translate_route(route, cities):
    return [cities[i][2] for i in route]
