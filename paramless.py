import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def point_mutation(vector, epsilon, **kwargs):
    """
    This is the simplest mutation function, it hits one single position of the vector and pushes it up (or down) by epsilon.
    """
    mutant = np.copy(vector)
    position = np.random.randint(len(vector))
    if (np.random.randint(2)):
        mutant[position] = mutant[position] + epsilon
    else:
        mutant[position] = mutant[position] - epsilon
    return mutant


def one_norm_distance(u, v):
    """
    Given two arrays returns the sum of position by position distances.
    Used as a distance function.
    """
    return np.sum(np.abs(u - v))


def target_function(x):
    """
    One target function for testing
    """
    return x ** 2.0


def distance_fitness_function(resident, mutant, target_surface, **kwargs):
    fitness_resident = 1.0 / one_norm_distance(resident, target_surface)
    fitness_mutant = 1.0 / one_norm_distance(mutant, target_surface)
    return fitness_resident, fitness_mutant


def evolution_step(resident_surface, fitness_function, mutation_function, **kwargs):
    """
    One generation iteration
    """
    invasion = False
    mutant = mutation_function(resident_surface, **kwargs)
    [fitness_resident, fitness_mutant] = fitness_function(
        resident_surface, mutant, **kwargs)
    if fitness_resident < fitness_mutant:
        resident_surface = np.copy(mutant)
        invasion = True
    return resident_surface, invasion


def evolve(initial_surface, fitness_function, mutation_function, iterations, return_time_series=False, seed=None, **kwargs):
    """
    Evolve to a target
    Returns a dict full of information, plus time series data if required
    """
    np.random.seed(seed)
    time_series = None
    last_entry_time = 0
    resident = np.copy(initial_surface)
    seq = 0
    time_series = None
    if return_time_series:
        time_series = []
    previous_resident = None
    for step in xrange(1, iterations):
        if return_time_series:
            previous_resident = np.copy(resident)
        resident, invasion = evolution_step(
            resident, fitness_function, mutation_function, **kwargs)
        if (return_time_series and invasion):
            time_series.append({
                               "seq": seq, "alive": step - last_entry_time, "resident": previous_resident})
            last_entry_time = step
            seq += 1
    if return_time_series:
        return resident, time_series
    else:
        return resident


def _update_line(frameid, time_series, frame_time_dict, domain, line, time_text):
    """
    Helper function to create video
    """
    time = frame_time_dict[frameid]
    line.set_data(domain, time_series[time])
    time_text.set_text("Generation: {}".format(time))
    return line, time_text,


def create_video_from_time_series(time_series, target_surface, domain, filename, approximate_number_of_frames):
    """
    Creates a video from a time series dict
    """
    # preliminaries

    # define a writer
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=50, metadata=dict(artist='Me'), bitrate=1800)
    # create figure with
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                         xlim=(min(domain) - 0.01, max(domain) + 0.01), ylim=(min(target_surface) - 0.01, max(target_surface) + 0.01))
    ax.grid()
    # plot the target
    ax.plot(domain, target_surface)
    # elements that change in the animatio
    l, = ax.plot([], [], 'r-')
    text_position_x = 0.02
    text_position_y = 0.02
    time_text = ax.text(
        text_position_x, text_position_y, '', transform=ax.transAxes)
    # create frameid:time dictionary with the actual surfaces to plot
    time_series_keys = time_series.keys()
    list_of_keys = np.sort(time_series_keys)[0::len(
        time_series_keys) / approximate_number_of_frames]
    frame_time_dict = dict()
    frame_identification = 0
    for key in list_of_keys:
        frame_time_dict[frame_identification] = key
        frame_identification += 1
    # once I have the plotting elements go ahead and create the animation
    line_ani = animation.FuncAnimation(
        fig, _update_line, len(list_of_keys), fargs=[time_series, frame_time_dict, domain, l, time_text],
        interval=1, blit=True)
    line_ani.save(filename, writer=writer)


def main():
    # initialize
    pass

if __name__ == '__main__':
    # main()
    pass
