# -*- coding: utf-8 -*-
'''
Created on 2013-08-14 12:59
@summary: Paramless evolution on a line
@author: garcia
'''
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import OrderedDict as OrderedDict
from copy import deepcopy as deepcopy

# default tolerance for float comparisons
DEFAULT_ATOL = 1e-8

#maximum iterations
MAX_ITERATIONS = 1000000

def _within_bounds(vector, lower_bound, upper_bound):
    '''
    @summary: Determines if the values of vector are in the [lower_bound, upper_bound] interval
    @param vector: surface to test
    @param lower_bound: lower_bound
    @param upper_bound: upper_bound
    @result: True or False 
    @todo: Add tolerance!
    '''
    if lower_bound != None and np.min(vector) < lower_bound :
        return False
    if upper_bound != None and np.max(vector) > upper_bound:
        return False
    return True


def _attemp_point_mutation(vector, mutation_epsilon):
    '''
    @summary: This is the simplest mutation function, it hits one single position of the vector and pushes it up (or down) by epsilon.
    If lower_bound and upper_bound are not None, it keeps the mutant bounded by only allowing in mutations that do not take things 
    out of bounds.
    @param vector: Parent surface to be mutated
    @param mutation_epsilon: epsilon of the perturbation
    @param lower_bound: default None, lower bound of the codomain if necessary
    @param upper_bound: default None, upper bound of the codomain if necessary
    @result: New mutant surface
    '''
    mutant = np.copy(vector)
    position = np.random.randint(len(vector))
    if (np.random.randint(2)):
        mutant[position] = mutant[position] + mutation_epsilon
    else:
        mutant[position] = mutant[position] - mutation_epsilon
    return mutant


def point_mutation(vector, mutation_epsilon, lower_bound=None, upper_bound=None, **kwargs):
    is_inside = False
    attemp = 0
    while (not is_inside):
        mutant = _attemp_point_mutation(vector, mutation_epsilon)
        is_inside=_within_bounds(mutant, lower_bound, upper_bound)
        attemp+=1
        if attemp > MAX_ITERATIONS:
            raise RuntimeError("Attempted too many mutations without producing anythin within bounds")
    return mutant


def point_mutation_distribution(vector, mutation_epsilon, **kwargs):
    # moves up a random point, and down a random point at the same time
    mutant = np.copy(vector)
    (position_up, position_down) = np.random.randint(len(vector), size=2)
    adjusted_epsilon = mutation_epsilon
    # taking care that no negative values are allowed
    if (mutant[position_down] - mutation_epsilon) < 0:
        adjusted_epsilon = mutant[position_down]
    mutant[position_up] = mutant[position_up] + adjusted_epsilon
    mutant[position_down] = mutant[position_down] - adjusted_epsilon
    return mutant


def _gaussian_mutation_helper(x, mutation_epsilon, loc, width):
    return mutation_epsilon * (math.e ** -(((x - loc) ** 2.0) / width))


def _attemp_gaussian_mutation(vector, mutation_epsilon, domain, width, lower_bound=None, upper_bound=None):
    location_index = np.random.randint(0, len(vector))
    location_value = domain[location_index]
    mutant = np.copy(vector)
    # upwards
    if (np.random.randint(2)):
        perturbation = _gaussian_mutation_helper(
            domain, mutation_epsilon=mutation_epsilon, loc=location_value, width=np.random.rand() * width)
        mutant += perturbation
    # downwards
    else:
        perturbation = _gaussian_mutation_helper(
            domain, mutation_epsilon=mutation_epsilon, loc=location_value, width=np.random.rand() * width)
        mutant -= perturbation
    return mutant

def gaussian_mutation(vector, mutation_epsilon, domain, width, lower_bound=None, upper_bound=None, **kwargs):
    is_inside = False
    attemp = 0
    while (not is_inside):
        mutant = _attemp_gaussian_mutation(vector, mutation_epsilon, domain, width, lower_bound=lower_bound, upper_bound=upper_bound)
        is_inside=_within_bounds(mutant, lower_bound, upper_bound)
        attemp+=1
        if attemp > MAX_ITERATIONS:
            raise RuntimeError("Attempted too many mutations without producing anythin within bounds")
    return mutant


def gaussian_mutation_distribution(vector, mutation_epsilon, domain, width, **kwargs):
    (location_index_up, location_index_down) = np.random.randint(
        len(vector), size=2)
    location_value_up = domain[location_index_up]
    location_value_down = domain[location_index_down]
    mutant = np.copy(vector)
    minimum_value = np.min(vector)
    if minimum_value - mutation_epsilon < 0:
        adjusted_epsilon = minimum_value
    else:
        adjusted_epsilon = mutation_epsilon
    width = np.random.rand() * width
    perturbation_up = _gaussian_mutation_helper(
        domain, mutation_epsilon=adjusted_epsilon, loc=location_value_up, width=width)
    perturbation_down = _gaussian_mutation_helper(
        domain, mutation_epsilon=adjusted_epsilon, loc=location_value_down, width=width)
    mutant += perturbation_up
    mutant -= perturbation_down
    return mutant


def one_norm_distance(u, v):
    """
    Given two arrays returns the sum of position by position distances.
    Used as a distance function.
    """
    return np.sum(np.abs(u - v))


def distance_fitness_function(resident, mutant, target_surface, **kwargs):
    fitness_resident = 1.0 / one_norm_distance(resident, target_surface)
    fitness_mutant = 1.0 / one_norm_distance(mutant, target_surface)
    return fitness_resident, fitness_mutant


def evolution_step(resident_surface, fitness_function, mutation_function, atol, *args, **kwargs):
    """
    One generation iteration
    """
    invasion = False
    mutant = mutation_function(resident_surface, **kwargs)
    [fitness_resident, fitness_mutant] = fitness_function(
        resident_surface, mutant, **kwargs)
    if fitness_resident < fitness_mutant and abs(fitness_resident - fitness_mutant) > atol:
        resident_surface = np.copy(mutant)
        invasion = True
    return resident_surface, invasion


def evolve(initial_surface, fitness_function, mutation_function, iterations, atol=DEFAULT_ATOL, return_time_series=False, seed=None, **kwargs):
    """
    Evolve 
    Returns last resident , plus time series data if required
    """
    np.random.seed(seed)
    time_series = None
    last_entry_time = 0
    resident = np.copy(initial_surface)
    seq = 0
    if return_time_series:
        time_series = OrderedDict()
    previous_resident = np.zeros_like(initial_surface)
    for step in xrange(1, iterations):
        if return_time_series:
            previous_resident = np.copy(resident)
        resident, invasion = evolution_step(
            resident, fitness_function, mutation_function, atol, **kwargs)
        if (return_time_series and invasion):
            time_series[seq] = {
                "alive": step - last_entry_time, "resident": previous_resident}
            last_entry_time = step
            seq += 1
    if return_time_series:
        return resident, time_series
    else:
        return resident


def _number_of_generations_in_summary_dict(summary_ordered_dict):
    """
    Given an Ordered dict with entries {seq: [resident, alive]}
    Counts the number of generations by summing up all the alive times
    """
    suma = 0
    for i in xrange(min(summary_ordered_dict.keys()), max(summary_ordered_dict.keys()) + 1):
        suma += summary_ordered_dict[i]['alive']
    return suma


def _update_line(frameid, time_series, frame_time_dict, domain, line, time_text):
    """
    Helper function to create video
    """
    time = frame_time_dict[frameid]
    line.set_data(domain, time_series[time])
    time_text.set_text("Generation: {}".format(time))
    return line, time_text,


def _expand_compact_time_series(series_compact, record_every):
    ans = OrderedDict()
    total_generations = _number_of_generations_in_summary_dict(series_compact)
    working_copy = deepcopy(series_compact)
    key_top = working_copy.keys()[0]
    for step in xrange(total_generations):
        if step % record_every == 0:
            ans[step] = working_copy[key_top]['resident']
        working_copy[key_top]['alive'] = working_copy[key_top]['alive'] - 1
        if working_copy[key_top]['alive'] == 0:
            del working_copy[key_top]
            if len(working_copy) > 0:
                key_top = working_copy.keys()[0]
    return ans


def create_video_from_time_series(series_compact, target_surface, domain, filename, approximate_number_of_frames, record_every, ylim=None, xlim=None):
    """
    Creates a video from a time series dict
    """
    # preliminaries
    # preprocess series
    time_series = _expand_compact_time_series(series_compact, record_every)
    # define a writer
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=50, metadata=dict(artist='Me'), bitrate=1800)
    # create figure with
    fig = plt.figure()
    if xlim is None or ylim is None:
        ylim = (-0.01, 3.0)
        xlim = (-0.01, 1.01)
    if target_surface is not None:
        ylim = (min(target_surface) - 0.01, max(target_surface) + 0.01)
        xlim = (min(domain) - 0.01, max(domain) + 0.01)
    ax = fig.add_subplot(111, aspect='auto', autoscale_on=False,
                         xlim=xlim, ylim=ylim)
    ax.grid()
    # plot the target
    if target_surface is not None:
        ax.plot(domain, target_surface)
    # elements that change in the animatio
    l, = ax.plot([], [], 'r-')
    text_position_x = 0.02
    text_position_y = 0.02
    time_text = ax.text(
        text_position_x, text_position_y, '', transform=ax.transAxes)
    # create frameid:time dictionary with the actual surfaces to plot
    time_series_keys = time_series.keys()
    interval = len(
        time_series_keys) / approximate_number_of_frames
    if interval <= 0:
        interval = 1
    list_of_keys = np.sort(time_series_keys)[0::interval]
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
    return line_ani


def main():
    pass
        

if __name__ == '__main__':
    main()
