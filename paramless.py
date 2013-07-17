import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt


def one_norm_distance(u, v):
    return np.sum(np.abs(u - v))


def mutate(vector, epsilon):
    mutant = np.copy(vector)
    position = np.random.randint(len(vector))
    if (np.random.randint(2)):
        mutant[position] = mutant[position] + epsilon
    else:
        mutant[position] = mutant[position] - epsilon
    return mutant


def target_function(x):
    return x ** 2.0


def evolution_step(resident_surface, target_surface, distance_function=one_norm_distance, **kwargs):
    mutant = mutate(resident_surface, **kwargs)
    distance_resident = distance_function(resident_surface, target_surface)
    distance_mutant = distance_function(mutant, target_surface)
    if distance_mutant < distance_resident:
        resident_surface = np.copy(mutant)
    return resident_surface


def update(frameid, x_evolving, number_of_generations, line, x, target):
    x_evolving = evolution_step(x_evolving, number_of_generations,
                        target_surface=target, distance_function=one_norm_distance)
    #print x_evolving, frameid
    line.set_xdata(x)
    line.set_ydata(x_evolving)


def main():
    # initialize
    number_of_generations = 1
    video_name = 'evolution.m4v'
    x = np.linspace(-1.0, 1.0, 10)  
    target = target_function(x)
    x_evolving = np.zeros_like(x)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, target_function(x))
    line, = ax.plot(x, target)
    ani = animation.FuncAnimation(
        fig, update, fargs=[x_evolving, number_of_generations, line, x, target], interval=200)
    ani.save(video_name, writer=animation.FFMpegFileWriter())

if __name__ == '__main__':
    #main()
    pass