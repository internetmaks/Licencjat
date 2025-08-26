import random
import numpy as np
from math import exp
from typing import List, Dict, Set
from .distance import distance_matrix
from .utils import route_is_valid

def feasible_start(num_cities: int, allowed: Dict[int, Set[int]]) -> List[int]:
    cities = list(allowed.keys())
    random.shuffle(cities)
    route = [None]*num_cities
    used = set()
    for c in cities:
        positions = list(allowed[c])
        random.shuffle(positions)
        placed = False
        for pos in positions:
            if pos not in used:
                route[pos] = c
                used.add(pos)
                placed = True
                break
        if not placed:
            return feasible_start(num_cities, allowed)
    # uzupełnianie
    for i in range(num_cities):
        if route[i] is None:
            for c in cities:
                if i in allowed[c] and c not in route:
                    route[i] = c
                    break
    return route

def neighbor(route: List[int], allowed: Dict[int, Set[int]], max_try=100) -> List[int]:
    r = route.copy()
    for _ in range(max_try):
        i, j = random.sample(range(len(r)), 2)
        ci, cj = r[i], r[j]
        if (i in allowed[cj]) and (j in allowed[ci]):
            r[i], r[j] = r[j], r[i]
            return r
    return r

def route_cost(route: List[int], M) -> float:
    s = 0.0
    for i in range(len(route)-1):
        s += M[route[i]][route[i+1]]
    return s

def run_sa(iterations=5000, t0=10000.0, cooling=0.95, allowed=None):
    M = distance_matrix()
    n = len(M)
    cur = feasible_start(n, allowed)
    cur_cost = route_cost(cur, M)
    best, best_cost = cur.copy(), cur_cost
    T = t0
    hist = []
    for _ in range(iterations):
        cand = neighbor(cur, allowed)
        c_cost = route_cost(cand, M)
        delta = c_cost - cur_cost
        if delta < 0:
            cur, cur_cost = cand, c_cost
        else:
            expo = -delta / max(T, 1e-12)
            prob = 0.0 if expo < -700 else exp(expo)
            if random.random() < prob:
                cur, cur_cost = cand, c_cost
        if cur_cost < best_cost:
            best, best_cost = cur.copy(), cur_cost
        T *= cooling
        hist.append(cur_cost)
    return best, best_cost, hist
