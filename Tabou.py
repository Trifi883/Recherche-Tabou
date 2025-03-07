import random

# Données du problème
distances = {
    'A': [10, 5, 15],  # Distances de A aux sites 1, 2, 3
    'B': [8, 12, 6],   # Distances de B aux sites 1, 2, 3
    'C': [15, 10, 8],  # Distances de C aux sites 1, 2, 3
    'D': [12, 7, 14]   # Distances de D aux sites 1, 2, 3
}
clients = ['A', 'B', 'C', 'D']
sites = [0, 1, 2]  # Indices des sites 
p = 2  # Nombre d'installations à placer

# Fonction pour calculer le coût total d'une solution
def calculate_cost(solution):
    total_cost = 0
    for client in clients:
        # Distance minimale entre le client et le site le plus proche dans la solution
        min_dist = min(distances[client][site] for site in solution)
        total_cost += min_dist
    return total_cost


# Générer les voisins d'une solution
def get_neighbors(solution, all_sites):
    neighbors = []
    for site_in in solution:  # Site à retirer
        for site_out in all_sites:
            if site_out not in solution:  # Site à ajouter
                neighbor = solution.copy()
                neighbor.remove(site_in)
                neighbor.add(site_out)
                neighbors.append(neighbor)
    return neighbors

# Algorithme de recherche taboue
def tabu_search(max_iterations, tabu_size):
    # Solution initiale aléatoire
    current_solution = set(random.sample(sites, p))
    best_solution = current_solution.copy()
    best_cost = calculate_cost(best_solution)
    
    # Liste taboue (on stocke les mouvements : tuple (site retiré, site ajouté))
    tabu_list = []
    
    # Itérations
    for iteration in range(max_iterations):
        # Générer les voisins
        neighbors = get_neighbors(current_solution, sites)
        
        # Trouver le meilleur voisin non tabou
        best_neighbor = None
        best_neighbor_cost = float('inf')
        
        for neighbor in neighbors:
            # Mouvement : quel site est retiré et ajouté
            site_removed = current_solution - neighbor
            site_added = neighbor - current_solution
            move = (site_removed.pop(), site_added.pop()) if site_removed else None
            
            # Vérifier si le mouvement est tabou
            if move and move in tabu_list:
                continue  # Ignorer si tabou
            
            cost = calculate_cost(neighbor)
            if cost < best_neighbor_cost:
                best_neighbor = neighbor
                best_neighbor_cost = cost
                next_move = move
        
        # Si aucun voisin valide n'est trouvé, arrêter
        if best_neighbor is None:
            break
        
        # Mettre à jour la solution courante
        current_solution = best_neighbor
        
        # Mettre à jour la meilleure solution si nécessaire
        if best_neighbor_cost < best_cost:
            best_solution = best_neighbor.copy()
            best_cost = best_neighbor_cost
        
        # Ajouter le mouvement à la liste taboue
        tabu_list.append(next_move)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)  # Retirer l'élément le plus ancien si la liste est pleine
        
        # Afficher l'état actuel
        print(f"Itération {iteration + 1}: Solution = {best_solution}, Coût = {best_cost}")
    
    return best_solution, best_cost

# Exécuter la recherche taboue
max_iterations = 10  # Nombre maximum d'itérations
tabu_size = 3        # Taille de la liste taboue
best_solution, best_cost = tabu_search(max_iterations, tabu_size)

# Résultat final
print(f"\nMeilleure solution trouvée : Sites {best_solution} avec un coût de {best_cost} km")