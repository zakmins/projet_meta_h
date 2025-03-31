import numpy as np
from data_modeling import MaxCoveringProblem

def fitness(solution, mcp):
    selected_subsets = [mcp.subsets[i] for i in range(mcp.n) if solution[i] == 1]
    covered_elements = set().union(*selected_subsets) if selected_subsets else set()
    penalty = max(0, sum(solution) - mcp.k) * 10  # Penalize exceeding k subsets
    return len(covered_elements) - penalty

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def pso(mcp, w, c1, c2, num_iterations):
    num_particles = 2 * mcp.n
    subsets_size = mcp.n

    particles = np.random.choice([0, 1], size=(num_particles, subsets_size))  # Random 0/1 solutions
    velocities = np.zeros((num_particles, subsets_size))  # Initial velocities

    personal_best = particles.copy()
    personal_best_scores = np.array([fitness(p, mcp) for p in particles])
    global_best = personal_best[np.argmax(personal_best_scores)]
    global_best_score = max(personal_best_scores)
    
    for iteration in range(num_iterations):
        for i in range(num_particles):
            r1, r2 = np.random.rand(), np.random.rand()
            velocities[i] = (
                w * velocities[i]
                + c1 * r1 * (personal_best[i] - particles[i])
                + c2 * r2 * (global_best - particles[i])
            )
            
            probabilities = sigmoid(velocities[i])
            particles[i] = np.where(np.random.rand(subsets_size) < probabilities, 1, 0)
            
            if sum(particles[i]) > mcp.k:
                excess = sum(particles[i]) - mcp.k
                ones_indices = np.where(particles[i] == 1)[0]
                np.random.shuffle(ones_indices)
                particles[i][ones_indices[:excess]] = 0  # Remove excess subsets
            
            score = fitness(particles[i], mcp)
            if score > personal_best_scores[i]:
                personal_best[i] = particles[i].copy()
                personal_best_scores[i] = score
                
                if score > global_best_score:
                    global_best = particles[i].copy()
                    global_best_score = score
        
        w *= 0.99  # Reduce inertia weight over time
        
        print(f"Iteration {iteration + 1}: Best Coverage = {global_best_score}, Selected Subsets = {global_best}")
    
    return global_best, global_best_score

if __name__ == "__main__":
    mcp = MaxCoveringProblem('./test/4/scp41.txt')
    w = 0.9  # Inertia weight
    c1 = 2.0  # Cognitive component
    c2 = 1.0  # Social component
    num_iterations = 100  # Number of iterations
    best_solution, best_score = pso(mcp, w, c1, c2, num_iterations)
    print("Final Best Solution:", best_solution)
    print("Maximum Covered Elements:", best_score)
