'''
Created on Mar 9, 2016

@author: Evan
'''

from collections import deque
from collections import OrderedDict
from copy import deepcopy

class DataPrep(object):
    '''
    classdocs
    '''


    def __init__(self, task_list, resource_list):
        '''
        Constructor
        '''
        self.tasks = self._create_mod_adj_list(task_list)
        self.resources = self._define_sort_rlist(resource_list)
        self.sorted_q = self._sudo_top_sort()
        
        
    def _sudo_top_sort(self):
        '''
        This method preforms sorting of the tasks list based on
        intertask dependencies.
        '''
        #create a deepcopy of the task list so we can modify it
        temp = deepcopy(self.tasks)
        unordered = self._check_zero_dep(temp) 
        zero_degree = deque([])
        sorted_queue = deque([])
    
        while temp:
            equal_list = {}
            for k in temp.keys():
                if not temp[k]['parent_tasks']:
                    #build a dictionary of equal priority tasks
                    equal_list[k] = temp[k]['child_task']
                    zero_degree.append(k)
                    #remove nodes with no incoming edges
                    del temp[k]
            #Prioritize the previously equal tasks by the task with the most children 
            equal_list = OrderedDict(sorted(equal_list.items(), key=lambda t: len(t[1]),reverse=True))      
            for k in equal_list.keys():
                #build the final sorted task list
                sorted_queue.append(k)
            #Topological sort by removing incoming edges from parents that have no incoming edges
            while zero_degree:   
                for k in temp.keys():          
                    if zero_degree[0] in temp[k]['parent_tasks']:
                        temp[k]['parent_tasks'].remove(zero_degree[0])
                zero_degree.popleft()   
        #Add the tasks with no priority to the end of the queue
        for i in unordered:
            sorted_queue.append(i)
            
        return sorted_queue
            
    def _check_zero_dep(self, temp):
        '''
        Checks for any tasks with no intertask dependencies
        '''
        
        unordered = []
        
        for k in temp.keys():  
            if not temp[k]['parent_tasks'] and not temp[k]['child_task']:
                unordered.append(k)
                del temp[k]
    
        return unordered
    
    def _create_mod_adj_list(self, tasks):
        '''
        Modifies the tasks to include child and parent lists.
        I made empty list values for parents to be more uniform
        when checking.
        '''    
        for k in tasks.keys():
            #initialize child task lists
            tasks[k]['child_task'] = []
            #create running state flag
            tasks[k]['running'] = False
            #create empty parent list for uniform parent checking
            if 'parent_tasks' not in tasks[k]:
                #create list for parents tasks if one does not exist
                tasks[k]['parent_tasks'] = []
            else:
                #change value from string format to list so its easier to remove an item
                tasks[k]['parent_tasks'] = tasks[k]['parent_tasks'].split(', ')           
            #check every tasks to see if it has a child task
            for i in tasks.keys():
                if 'parent_tasks' in tasks[i]:
                    if k in tasks[i]['parent_tasks']:
                        tasks[k]['child_task'].append(i)
                        
        return tasks
                        
    def _define_sort_rlist(self, resources):
        '''
        Adds extra keys for the scheduler to use and sorts based on least cores
        so that the scheduler can start out by assigning tasks resources with the least cores possible
        
        The algorithm used in scheduler does NOT try to optimize cores by predicting the 
        if a certain high core resource will be locked for a long period of time which could lead to issues
        if a task has many children needed and needs many cores.
        '''
        
        for k in resources.keys():
            resources[k]={'cores': resources[k], 'time': 0, 'c_task':''}
        #sort the resources with least cores in the front
        resources = OrderedDict(sorted(resources.items(), key=lambda t: t[1]['cores']))
        return resources