import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from schedule_opt.data import ALLOWED_POSITIONS, CITIES
from schedule_opt.ga import run_ga
from schedule_opt.distance import distance_matrix
from schedule_opt.utils import translate_route

def generate_convergence_plots(best_histories_by_key):
    os.makedirs("wyniki_wykresy", exist_ok=True)
    # mutacja dla 500 generacji
    fig = plt.figure(figsize=(12,8))
    for mut, histories in best_histories_by_key.get("mut_500", {}).items():
        if not histories: continue
        max_len = min(len(h) for h in histories)
        avg = [np.mean([h[i] for h in histories]) for i in range(max_len)]
        plt.plot(range(len(avg)), avg, label=f"Mutacja={mut}")
    plt.title("Wpływ mutacji (500 generacji)")
    plt.xlabel("Iteracja"); plt.ylabel("Średni dystans (km)"); plt.grid(True); plt.legend(); plt.tight_layout()
    plt.savefig("wyniki_wykresy/wplyw_mutacji_gen500.png", dpi=300); plt.close(fig)

    # mutacja dla 1000 generacji
    fig = plt.figure(figsize=(12,8))
    for mut, histories in best_histories_by_key.get("mut_1000", {}).items():
        if not histories: continue
        max_len = min(len(h) for h in histories)
        avg = [np.mean([h[i] for h in histories]) for i in range(max_len)]
        plt.plot(range(len(avg)), avg, label=f"Mutacja={mut}")
    plt.title("Wpływ mutacji (1000 generacji)")
    plt.xlabel("Iteracja"); plt.ylabel("Średni dystans (km)"); plt.grid(True); plt.legend(); plt.tight_layout()
    plt.savefig("wyniki_wykresy/wplyw_mutacji_gen1000.png", dpi=300); plt.close(fig)

    # wykres wedlug populacji
    fig = plt.figure(figsize=(12,8))
    for pop, histories in best_histories_by_key.get("pop", {}).items():
        if not histories: continue
        max_len = min(len(h) for h in histories)
        avg = [np.mean([h[i] for h in histories]) for i in range(max_len)]
        plt.plot(range(len(avg)), avg, label=f"Populacja={pop}")
    plt.title("Wpływ populacji na zbieżność")
    plt.xlabel("Iteracja"); plt.ylabel("Średni dystans (km)"); plt.grid(True); plt.legend(); plt.tight_layout()
    plt.savefig("wyniki_wykresy/wplyw_populacji_zbieznosc.png", dpi=300); plt.close(fig)

def main():
    populacje = [50, 100, 200]
    generacje = [500, 1000]
    mutacje = [0.01, 0.05, 0.1, 0.2]
    turniej_frac = [0.4]
    proby = 5
    penalty = 50000.0

    print("=== GRID GA ===")
    total = len(populacje)*len(generacje)*len(mutacje)*len(turniej_frac)
    wyniki = []
    najlepsze_trasy = {}
    historie_kombinacji = {}
    M = distance_matrix()

    start_all = time.time()
    combo_i = 0
    for pop in populacje:
        for gen in generacje:
            for mut in mutacje:
                for tf in turniej_frac:
                    combo_i += 1
                    key = f"pop{pop}_gen{gen}_mut{mut}_tur{tf}"
                    print(f"\n[{combo_i}/{total}] {key}")
                    dystanse, czasy, historie = [], [], []
                    best_route, best_real, best_hist = None, float('inf'), None
                    for p in range(proby):
                        t0 = time.time()
                        r, real, hist = run_ga(population_size=pop, generations=gen, pmut=mut,
                                               tournament_frac=tf, allowed=ALLOWED_POSITIONS, penalty=penalty)
                        t1 = time.time()
                        czasy.append(t1 - t0)
                        historie.append(hist)
                        dystanse.append(real)
                        if real < best_real:
                            best_real = real; best_route = r.copy(); best_hist = hist.copy()
                        print(f"  Probe {p+1}/{proby}: dist={real:.2f} time={t1-t0:.2f}s")
                    # statystyki
                    avg_d = float(np.mean(dystanse)) if dystanse else float('inf')
                    min_d = float(np.min(dystanse)) if dystanse else float('inf')
                    std_d = float(np.std(dystanse)) if len(dystanse)>1 else 0.0
                    avg_t = float(np.mean(czasy)) if czasy else 0.0
                    wyniki.append({
                        "Populacja": pop, "Generacje": gen, "Mutacja": mut, "Turniej%": tf,
                        "Średni_dystans": avg_d, "Min_dystans": min_d, "Std_dystans": std_d, "Średni_czas": avg_t
                    })
                    if best_route is not None:
                        najlepsze_trasy[key] = {
                            "trasa": best_route, "dystans": best_real,
                            "parametry": {"populacja": pop, "generacje": gen, "mutacja": mut, "turniej": tf},
                            "historia": best_hist
                        }
                    historie_kombinacji[key] = {"historie": historie, "parametry": {"populacja": pop, "generacje": gen, "mutacja": mut, "turniej": tf}}
    # podsumowanie
    os.makedirs("wyniki", exist_ok=True)
    df = pd.DataFrame(wyniki)
    df.to_csv("wyniki/wyniki_ga.csv", index=False)

    # wykres zbieżności
    buckets = {"mut_500": {}, "mut_1000": {}, "pop": {}}
    for k, v in najlepsze_trasy.items():
        gen = v["parametry"]["generacje"]; mut = v["parametry"]["mutacja"]; pop = v["parametry"]["populacja"]
        h = v.get("historia", [])
        if gen == 500:
            buckets["mut_500"].setdefault(mut, []).append(h)
        if gen == 1000:
            buckets["mut_1000"].setdefault(mut, []).append(h)
        buckets["pop"].setdefault(pop, []).append(h)
    generate_convergence_plots(buckets)

    # znalezione optimum
    if najlepsze_trasy:
        best = min(najlepsze_trasy.values(), key=lambda x: x["dystans"])
        print("\nBEST GLOBAL:")
        print(best["parametry"], best["dystans"], translate_route(best["trasa"], CITIES))

if __name__ == "__main__":
    main()
