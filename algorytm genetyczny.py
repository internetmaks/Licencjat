import random
import numpy as np
from typing import List, Tuple, Dict, Set
from .distance import distance_matrix
from .utils import route_is_valid

def objective(route: List[int], M, allowed: Dict[int, Set[int]], penalty: float):
    r = np.array(route)
    dist = float(np.sum(M[r[:-1], r[1:]]))
    # dodanie karnego dystansu za przekroczenie ogarniczen
    pen = 0.0
    for city_idx, allowed_pos in allowed.items():
        pos = route.index(city_idx)
        if pos not in allowed_pos:
            pen += penalty
    return dist + pen

def init_population(pop_size: int, num_cities: int):
    pop = []
    base = list(range(num_cities))
    for _ in range(pop_size):
        random.shuffle(base)
        pop.append(base.copy())
    return pop

def tournament(pop, M, tsize, allowed, penalty):
    candidates = random.sample(pop, tsize)
    return min(candidates, key=lambda x: objective(x, M, allowed, penalty))

def pmx_crossover(p1: List[int], p2: List[int]) -> Tuple[List[int], List[int]]:
    size = len(p1)
    a, b = sorted(random.sample(range(size), 2))
    c1, c2 = p1.copy(), p2.copy()
    map12 = {p1[i]: p2[i] for i in range(a, b+1)}
    map21 = {p2[i]: p1[i] for i in range(a, b+1)}
    for i in list(range(0, a)) + list(range(b+1, size)):
        g = p2[i]
        while g in map12:
            g = map12[g]
        c1[i] = g
        g = p1[i]
        while g in map21:
            g = map21[g]
        c2[i] = g
    return c1, c2

def swap_mutation(ind: List[int], pmut: float) -> List[int]:
    child = ind.copy()
    if random.random() < pmut:
        i, j = random.sample(range(len(child)), 2)
        child[i], child[j] = child[j], child[i]
    return child

def run_ga(population_size=200, generations=1000, pmut=0.1, tournament_frac=0.4,
           allowed=None, penalty=50000.0, save_history=True):
    M = distance_matrix()
    n = len(M)
    tsize = max(2, int(population_size * tournament_frac))
    pop = init_population(population_size, n)
    history = []
    best, best_cost = None, float("inf")

    for g in range(generations):
        current = min(pop, key=lambda x: objective(x, M, allowed, penalty))
        current_cost = objective(current, M, allowed, penalty)
        if current_cost < best_cost:
            best_cost, best = current.copy(), current_cost
        new_pop = []
        while len(new_pop) < population_size:
            p1 = tournament(pop, M, tsize, allowed, penalty)
            p2 = tournament(pop, M, tsize, allowed, penalty)
            c1, c2 = pmx_crossover(p1, p2)
            c1 = swap_mutation(c1, pmut)
            c2 = swap_mutation(c2, pmut)
            if route_is_valid(c1, allowed, n): new_pop.append(c1)
            else: new_pop.append(p1)
            if len(new_pop) < population_size:
                if route_is_valid(c2, allowed, n): new_pop.append(c2)
                else: new_pop.append(p2)
        pop = new_pop
        if save_history:
            history.append(best_cost)
    # oblicz dystans bez kar
    real = 0.0
    for i in range(len(best)-1):
        real += M[best[i]][best[i+1]]
    return best, real, history
