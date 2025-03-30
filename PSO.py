import numpy as np  # type: ignore
import random
from data_modeling import MaxCoveringProblem

def fitness(solution, subsets):
    """ Compute fitness: number of unique elements covered """
    covered = set()
    for i, selected in enumerate(solution):
        if selected:  # If subset is selected
            covered.update(subsets[i])
    return len(covered)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def initialize_particles(num_particles, num_subsets, k):
    """ Initialize particles with k randomly selected subsets """
    particles = []
    for _ in range(num_particles):
        particle = np.zeros(num_subsets, dtype=int)
        indices = random.sample(range(num_subsets), k)
        particle[indices] = 1
        particles.append(particle)
    return np.array(particles)

def particle_swarm_optimization(mcp, num_particles=30, max_iter=100, w=0.7, c1=1.5, c2=1.5):
    """ PSO Algorithm for Maximum Covering Problem """
    particles = initialize_particles(num_particles, mcp.n, mcp.k)
    velocities = np.random.uniform(-1, 1, (num_particles, mcp.n))  # Initialize velocities
    personal_best = particles.copy()
    personal_best_fitness = np.array([fitness(p, mcp.subsets) for p in particles])
    global_best = personal_best[np.argmax(personal_best_fitness)]
    global_best_fitness = max(personal_best_fitness)
    
    for _ in range(max_iter):
        for i in range(num_particles):
            r1, r2 = np.random.rand(), np.random.rand()
            velocities[i] = (w * velocities[i] +
                             c1 * r1 * (personal_best[i] - particles[i]) +
                             c2 * r2 * (global_best - particles[i]))
            
            # Convert velocity to probability and update position
            probabilities = sigmoid(velocities[i])
            new_particle = (np.random.rand(mcp.n) < probabilities).astype(int)
            
            # Ensure exactly k subsets are selected
            if np.sum(new_particle) != mcp.k:
                selected_indices = np.where(new_particle == 1)[0]
                if len(selected_indices) > mcp.k:  # Too many selected
                    to_remove = np.random.choice(selected_indices, len(selected_indices) - mcp.k, replace=False)
                    new_particle[to_remove] = 0
                elif len(selected_indices) < mcp.k:  # Too few selected
                    available_indices = np.where(new_particle == 0)[0]
                    to_add = np.random.choice(available_indices, mcp.k - len(selected_indices), replace=False)
                    new_particle[to_add] = 1
            
            particles[i] = new_particle
            
            # Update personal and global bests
            current_fitness = fitness(particles[i], mcp.subsets)
            if current_fitness > personal_best_fitness[i]:
                personal_best[i] = particles[i].copy()
                personal_best_fitness[i] = current_fitness
            if current_fitness > global_best_fitness:
                global_best = particles[i].copy()
                global_best_fitness = current_fitness
    
    return global_best, global_best_fitness

file_path = "./test/4/scp41.txt"  # Replace with your actual SCP file
mcp = MaxCoveringProblem(file_path)
best_solution, best_coverage = particle_swarm_optimization(mcp)
print("Best solution:", best_solution)
print("Elements covered:", best_coverage)
