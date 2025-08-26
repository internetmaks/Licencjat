import math
import numpy as np
from .data import CITIES

def haversine_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6371.0 * c

def distance_matrix():
    n = len(CITIES)
    M = np.zeros((n, n), dtype=float)
    for i in range(n):
        lat1, lon1, _ = CITIES[i]
        for j in range(n):
            if i == j:
                continue
            lat2, lon2, _ = CITIES[j]
            M[i, j] = haversine_km(lat1, lon1, lat2, lon2)
    return np.around(M, 2)