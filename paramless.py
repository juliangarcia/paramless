import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def one_norm_distance(u, v):
    """
    Given two arrays returns the sum of position by position distances.
    Used as a distance function.
    """
    return np.sum(np.abs(u - v))


def point_mutation(vector, epsilon):
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


def target_function(x):
    """
    One target function for testing
    """
    return x ** 2.0


def evolution_step(resident_surface, target_surface, mutation_function=point_mutation, distance_function=one_norm_distance, **kwargs):
    """
    One generation iteration
    """
    mutant = mutation_function(resident_surface, **kwargs)
    distance_resident = distance_function(resident_surface, target_surface)
    distance_mutant = distance_function(mutant, target_surface)
    if distance_mutant < distance_resident:
        resident_surface = np.copy(mutant)
        distance_resident = distance_mutant
    return resident_surface, distance_resident


def evolve(initial_surface, target_surface, mutation_function, distance_function, target_distance, maximum_iterations=100000, return_time_series=False, record_interval=1000, **kwargs):
    """
    Evolve to a target
    Returns a dict full of information, plus time series data if required
    """
    time_series = None
    if return_time_series:
        time_series = dict()
    resident = np.copy(initial_surface)
    for step in xrange(maximum_iterations):
        resident, distance_resident = evolution_step(
            resident, target_surface, mutation_function, distance_function, **kwargs)
        if distance_resident < target_distance:
            return {"evolved_surface": resident, "distance to target": distance_resident, "number_of_steps": step, "finished": True}, time_series
        if (return_time_series and (step % record_interval == 0)):
            time_series[step] = resident.copy()
    return {"evolved_surface": resident, "distance to target": distance_resident, "number_of_steps": step, "finished": False}, time_series


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

    #define a writer
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=50, metadata=dict(artist='Me'), bitrate=1800)
    #create figure with
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                         xlim=(min(domain) - 0.01, max(domain) + 0.01), ylim=(min(target_surface) - 0.01, max(target_surface) + 0.01))
    ax.grid()
    #plot the target
    ax.plot(domain, target_surface)
    #elements that change in the animatio
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
    #once I have the plotting elements go ahead and create the animation
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
