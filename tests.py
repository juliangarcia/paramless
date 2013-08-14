'''
Created on Jan 31, 2013

@author: garcia
'''
import unittest
import numpy as np
from paramless import _within_bounds as within_bounds
from paramless import point_mutation as point_mutation
from paramless import gaussian_mutation as gaussian_mutation

class Test(unittest.TestCase):

    def testPointMutationWithBounds(self):
        x = np.linspace(0.01, 1.0, 100, endpoint=True)
        parent = np.zeros_like(x)
        mutant = point_mutation(parent, mutation_epsilon= 0.2, lower_bound=0.0, upper_bound=0.5)
        self.assertTrue(np.max(mutant)<= 0.5)
        self.assertTrue(np.min(mutant)>= 0.0)


    def testGaussianMutationWithBounds(self):
        x = np.linspace(0.01, 1.0, 100, endpoint=True)
        parent = np.zeros_like(x)
        mutant = gaussian_mutation(parent, mutation_epsilon=0.2, domain=x, width=0.01, lower_bound=0.0, upper_bound=0.5)
        self.assertTrue(np.max(mutant)<= 0.5)
        self.assertTrue(np.min(mutant)>= 0.0)



    def testWithinBounds(self):
        zeroes_vector = np.zeros(10)
        self.assertTrue(within_bounds(zeroes_vector, lower_bound=-1.0, upper_bound=1.0), "test 1")
        self.assertTrue(within_bounds(zeroes_vector, lower_bound=0.0, upper_bound=1.0), "test 2")
        ones_vector = np.ones(10)
        self.assertTrue(within_bounds(ones_vector, lower_bound=0.0, upper_bound=1.0), "test 3")
        self.assertFalse(within_bounds(ones_vector, lower_bound=0.0, upper_bound=0.5), "test 4")
        self.assertTrue(within_bounds(ones_vector, lower_bound=None, upper_bound=None), "test 5")
        
        
if __name__ == "__main__":
    unittest.main()