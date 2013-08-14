'''
Created on Jan 31, 2013

@author: garcia
'''
import unittest
import numpy as np
from paramless import within_bounds

class Test(unittest.TestCase):

    # def testPointMutationWithBounds(self):
    #     x = np.linspace(0.01, 1.0, 100, endpoint=True)
    #     parent = np.zeros_like(x)
    #     self.assertTrue(np.max(point_mutation(parent, mutation_epsilon= 0.8, lower_bound=0.0, upper_bound=0.5))<= 0.5)
    #     self.assertTrue(np.min(point_mutation(parent, mutation_epsilon= 0.8, lower_bound=0.0, upper_bound=0.5))>= 0.0)


    def testWithinBounds(self):
        zeroes_vector = np.zeros(10)
        self.assertTrue(within_bounds(zeroes_vector, lower_bound=-1.0, upper_bound=1.0), "test 1")
        self.assertTrue(within_bounds(zeroes_vector, lower_bound=0.0, upper_bound=1.0), "test 2")
        ones_vector = np.ones(10)
        self.assertTrue(within_bounds(ones_vector, lower_bound=0.0, upper_bound=1.0), "test 3")
        self.assertFalse(within_bounds(ones_vector, lower_bound=0.0, upper_bound=0.5), "test 4")
        
        
if __name__ == "__main__":
    unittest.main()