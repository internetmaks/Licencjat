import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from schedule_opt.data import ALLOWED_POSITIONS, CITIES
from schedule_opt.sa import run_sa
from schedule_opt.utils import translate_route

def main():
    pop_sizes = [20, 50, 100, 200]  
    coolings = [0.99, 0.95, 0.90, 0.80]
    iterations = 5000
    t0 = 10000.0
    runs = 5

    print("=== GRID SA ===")
    results = []
    os.makedirs("wykresy", exist_ok=True)

    for pop in pop_sizes:
        for cool in coolings:
            print(f"\nTesting: population_size={pop}, cooling={cool}")
            costs = []
            histories = []
            for r in range(runs):
                print(f" Run {r+1}/{runs}")
                t_start = time.time()
                route, cost, hist = run_sa(iterations=iterations, t0=t0, cooling=cool, allowed=ALLOWED_POSITIONS)
                t_end = time.time()
                print(f"  Cost: {cost:.2f} km, Time: {t_end - t_start:.2f}s")
                costs.append(cost); histories.append(hist)
            avg_cost = float(np.mean(costs)); std_cost = float(np.std(costs))
            results.append({"population_size": pop, "cooling": cool, "avg_cost": avg_cost, "std_cost": std_cost,
                            "best_cost": float(np.min(costs)), "worst_cost": float(np.max(costs))})
            #średnia
            min_len = min(len(h) for h in histories)
            histories = [h[:min_len] for h in histories]
            avg_hist = list(np.mean(histories, axis=0))
            plt.figure(figsize=(10,6))
            plt.plot(avg_hist)
            plt.title(f"pop={pop}, cooling={cool}\\nAvg cost: {avg_cost:.2f} ± {std_cost:.2f} km")
            plt.xlabel("Iteracja"); plt.ylabel("Koszt (km)")
            plt.savefig(f"wykresy/sa_pop_{pop}_cool_{cool}.png", dpi=300); plt.close()

    pd.DataFrame(results).to_csv("wyniki_sa.csv", index=False)

if __name__ == "__main__":
    main()