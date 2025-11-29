import random
import math

# -----------------------------------------
# Tính khoảng cách Euclid giữa hai thành phố
# -----------------------------------------
def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# -----------------------------------------
# Tính tổng quãng đường của 1 tour
# -----------------------------------------
def total_distance(route, cities):
    dist = 0
    for i in range(len(route)):
        dist += distance(cities[route[i]], cities[route[(i+1) % len(route)]])
    return dist

# -----------------------------------------
# Khởi tạo ngẫu nhiên một cá thể (một hoán vị)
# -----------------------------------------
def create_individual(n):
    route = list(range(n))
    random.shuffle(route)
    return route

# -----------------------------------------
# Chọn lọc theo Tournament Selection
# -----------------------------------------
def selection(population, fitnesses, k=3):
    selected = random.sample(list(zip(population, fitnesses)), k)
    selected.sort(key=lambda x: x[1])
    return selected[0][0]

# -----------------------------------------
# Lai ghép PMX (Partially Mapped Crossover)
# -----------------------------------------
def pmx_crossover(parent1, parent2):
    size = len(parent1)
    child = [-1] * size

    a, b = sorted(random.sample(range(size), 2))

    # Copy đoạn giữa
    child[a:b] = parent1[a:b]

    # Fill các gene còn lại từ parent2
    for i in range(a, b):
        if parent2[i] not in child:
            pos = i
            val = parent2[i]
            while child[pos] != -1:
                pos = parent2.index(parent1[pos])
            child[pos] = val

    for i in range(size):
        if child[i] == -1:
            child[i] = parent2[i]

    return child

# -----------------------------------------
# Đột biến – nhập hoán vị 2 vị trí
# -----------------------------------------
def mutate(route, mutation_rate=0.05):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]
    return route

# -----------------------------------------
# GA chính
# -----------------------------------------
def genetic_algorithm_tsp(cities, population_size=100, 
                          crossover_rate=0.9, mutation_rate=0.05, 
                          generations=300):

    n = len(cities)
    population = [create_individual(n) for _ in range(population_size)]

    for gen in range(generations):

        fitnesses = [total_distance(ind, cities) for ind in population]
        new_population = []

        # Lưu cá thể tốt nhất
        best_idx = min(range(population_size), key=lambda i: fitnesses[i])
        best = population[best_idx]
        best_fit = fitnesses[best_idx]

        # In tiến trình (tùy chọn)
        if gen % 50 == 0:
            print(f"Gen {gen}, Best distance: {best_fit:.3f}")

        # Tạo thế hệ mới
        while len(new_population) < population_size:
            parent1 = selection(population, fitnesses)
            parent2 = selection(population, fitnesses)

            # Crossover
            if random.random() < crossover_rate:
                child = pmx_crossover(parent1, parent2)
            else:
                child = parent1[:]

            # Mutation
            child = mutate(child, mutation_rate)

            new_population.append(child)

        population = new_population

    # Kết quả cuối
    fitnesses = [total_distance(ind, cities) for ind in population]
    best_idx = min(range(population_size), key=lambda i: fitnesses[i])

    return population[best_idx], fitnesses[best_idx]

# -----------------------------------------
# DEMO CHẠY THỬ
# -----------------------------------------
if __name__ == "__main__":
    # Tọa độ thành phố (10 thành phố)
    cities = [
        (0, 0), (1, 5), (5, 2), (3, 3), (7, 6),
        (2, 8), (6, 1), (8, 8), (9, 3), (4, 7)
    ]

    best_route, best_distance = genetic_algorithm_tsp(cities)

    print("\nBest Route Found:", best_route)
    print("Best Distance:", best_distance)