import numpy as np


def one_norm_distance(u, v):
    return np.sum(np.abs(u - v))


def point_mutation(vector, epsilon):
    mutant = np.copy(vector)
    position = np.random.randint(len(vector))
    if (np.random.randint(2)):
        mutant[position] = mutant[position] + epsilon
    else:
        mutant[position] = mutant[position] - epsilon
    return mutant


def target_function(x):
    return x ** 2.0


def evolution_step(resident_surface, target_surface, mutation_function=point_mutation, distance_function=one_norm_distance, **kwargs):
    mutant = mutation_function(resident_surface, **kwargs)
    distance_resident = distance_function(resident_surface, target_surface)
    distance_mutant = distance_function(mutant, target_surface)
    if distance_mutant < distance_resident:
        resident_surface = np.copy(mutant)
    return resident_surface


def main():
    # initialize
    pass

if __name__ == '__main__':
    #main()
    pass
