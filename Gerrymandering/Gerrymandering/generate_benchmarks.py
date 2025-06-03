import random
import os

def generate_instance(filepath, M, N, K, vote_distribution_func):
    with open(filepath, 'w') as f:
        f.write(f"grid_size({M},{N}).\n")
        f.write(f"num_districts({K}).\n\n")

        f.write("% Cells\n")
        for r in range(1, M + 1):
            for c in range(1, N + 1):
                f.write(f"cell({r},{c}).\n")
        f.write("\n")

        f.write("% Votes\n")
        for r in range(1, M + 1):
            for c in range(1, N + 1):
                party = vote_distribution_func(r, c, M, N)
                f.write(f"vote({r},{c},{party}).\n")

# --- Vote Distribution Strategies ---
def random_votes(r, c, M, N):
    return random.choice([0, 1])

def clustered_votes(r, c, M, N, party0_center_r=None, party0_center_c=None, radius_factor=0.3):
    if party0_center_r is None: party0_center_r = M / 2
    if party0_center_c is None: party0_center_c = N / 2
    # Simple clustering: higher chance of party 0 near its "center"
    distance = ((r - party0_center_r)**2 + (c - party0_center_c)**2)**0.5
    max_dist = ((M**2 + N**2)**0.5) * radius_factor
    if distance < max_dist:
        return 0 if random.random() < 0.75 else 1 # 75% chance of party 0 if close
    else:
        return 1 if random.random() < 0.75 else 0 # 75% chance of party 1 if far

def checkerboard_votes(r, c, M, N):
    return (r + c) % 2

# --- Benchmark Generation Loop ---
if not os.path.exists("benchmarks"):
    os.makedirs("benchmarks")

instance_count = 0
m_n_k_combinations = [
    # Small
    (3, 3, 2), (4, 3, 2), (4, 4, 3), (5, 4, 3),
    # Medium
    (5, 5, 3), (6, 5, 4), (7, 6, 4), (8, 8, 5),
    # Potentially harder (might hit timeout)
    (10, 8, 5), (10, 10, 6) 
]

vote_strats = {
    "random": random_votes,
    "clustered": clustered_votes,
    "checkerboard": checkerboard_votes
}

target_benchmarks = 100
created_benchmarks = 0

for m, n, k in m_n_k_combinations:
    if created_benchmarks >= target_benchmarks:
        break
    for strat_name, strat_func in vote_strats.items():
        if created_benchmarks >= target_benchmarks:
            break
        
        # For clustered, maybe try a few different centers or radii if desired
        # For simplicity, using default center here
        
        # Ensure K is not too large for the grid size
        if k > m * n:
            print(f"Skipping M={m},N={n},K={k} as K > M*N")
            continue
        # Ensure at least one cell per district on average (very rough heuristic)
        if m * n / k < 1: # or some other threshold like 2 or 3 for meaningful districts
            print(f"Skipping M={m},N={n},K={k} due to too many districts for grid size.")
            continue


        filename = f"benchmarks/instance_{created_benchmarks+1:03d}_m{m}n{n}k{k}_{strat_name}.lp"
        generate_instance(filename, m, n, k, strat_func)
        print(f"Generated: {filename}")
        created_benchmarks += 1
        if created_benchmarks % 5 == 0 and strat_name == "clustered": # Add more clustered variations
             # Example: shift cluster center for variety
            def custom_clustered(r_c, c_c, M_c, N_c):
                return clustered_votes(r_c,c_c,M_c,N_c, M_c*0.25, N_c*0.25)
            filename = f"benchmarks/instance_{created_benchmarks+1:03d}_m{m}n{n}k{k}_{strat_name}_v2.lp"
            generate_instance(filename, m, n, k, custom_clustered)
            print(f"Generated: {filename}")
            created_benchmarks +=1


# Fill up to 100 with more randoms on varied sizes if needed
idx = 0
while created_benchmarks < target_benchmarks:
    m, n, k = random.choice(m_n_k_combinations)
    if k > m*n or m*n/k < 1: continue

    strat_name, strat_func = random.choice(list(vote_strats.items()))
    
    filename = f"benchmarks/instance_{created_benchmarks+1:03d}_m{m}n{n}k{k}_{strat_name}_extra{idx}.lp"
    generate_instance(filename, m, n, k, strat_func)
    print(f"Generated: {filename}")
    created_benchmarks += 1
    idx +=1

print(f"\nTotal benchmarks generated: {created_benchmarks}")