'''
Created on Mar 10, 2016

@author: Evan
'''
import unittest
from data_prep import DataPrep
from collections import OrderedDict
from collections import deque


class Test(unittest.TestCase):


    def setUp(self):
        tasks ={'task1': {'execution_time': 100, 'cores_required': 2},
                'task2': {'execution_time': 200, 'cores_required': 1, 'parent_tasks': 'task1'},
                'task3': {'execution_time': 50, 'cores_required': 4, 'parent_tasks': 'task1, task2'}}#,'task4': {'execution_time': 100, 'cores_required': 2}}        
        resources = {'compute1': 2, 'compute3': 6, 'compute2': 2}

        self.data = DataPrep(tasks, resources)


    def tearDown(self):
        pass


    def test_sorted_resources(self):
  
        sorted_correctly = OrderedDict([('compute1', {'cores': 2, 'c_task': '', 'time': 0}), 
                                        ('compute2', {'cores': 2, 'c_task': '', 'time': 0}), 
                                        ('compute3', {'cores': 6, 'c_task': '', 'time': 0})])
        self.assertEqual(self.data.resources,sorted_correctly)
        
    def test_sorted_tasks(self):
        sorted_correctly = deque(['task1', 'task2', 'task3']) 
        self.assertEqual(self.data.sorted_q,sorted_correctly)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()