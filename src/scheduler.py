#!/usr/bin/env python
'''
Created on Mar 6, 2016

@author: Evan
'''
import sys
from collections import deque
from collections import OrderedDict

from io_yaml import IOYaml
from arg_processor import ArgProcessor
from data_prep import DataPrep

class Scheduler(object):
    '''
    This class contains the algorithm for
    building the schedule
    '''
     
    def __init__(self, schedule_data):
        '''
        Constructor
        '''
        self._data = schedule_data
        self._schedule = OrderedDict({})
        
    def gen_schedule(self):
 
        p_queue = deque([])
        self._recurs_sch(self._data.sorted_q, p_queue)
        return self._schedule
        
    def _down_tick(self):
        '''
        Decrement the time of all resources not at 0 by 
        the amount of time left on the resource with the
        least time left 
        '''
        #get the resource with least time left by removing all resources with time at 0
        least_time = OrderedDict(filter(lambda t: t[1]['time']!=0, self._data.resources.items()))
        #sorting by the least amount of time
        least_time = OrderedDict(sorted(least_time.items(), key=lambda t: t[1]['time']))
        #getting the least time resource by index
        least_time = least_time.items()[0]
        
        #loop through resources and decrement the time  if the time is not already at 0
        for r in self._data.resources.keys():
            if self._data.resources[r]['time']>0:
                self._data.resources[r]['time'] -= least_time[1]['time']
                #if the time is now at 0, mark the resource as available
                if self._data.resources[r]['time'] == 0 and self._data.resources[r]['c_task'] != '':
                    #set the task as no longer running
                    self._data.tasks[self._data.resources[r]['c_task']]['running'] = False;
                    self._data.resources[r]['c_task'] = ''
                    
    def _recurs_sch(self,c_queue,p_queue):
        '''
        This method uses to queue and recursion
        to construct the schedule. The two queues are
        the current queue and pending queue. If a task 
        cannot be scheduled because it is blocked.
        The task is moved to the pending queue. When the
        current queue is empty the function recurses 
        swapping the queues.
        '''
        if not c_queue:
            return 
        if self._check_p_running(c_queue):
            p_queue.append(c_queue.popleft())
            if not c_queue:
                self._down_tick()
                return self._recurs_sch(p_queue, c_queue)
            else:
                return self._recurs_sch(c_queue, p_queue)
        #If a resource is available, set the relevant data and add the task+sched to the schedule
        for resource in self._data.resources.keys():
            if self._data.resources[resource]['time'] == 0:            
                if self._data.resources[resource]['cores']>= self._data.tasks[c_queue[0]]['cores_required']:
                    self._data.resources[resource]['time'] = self._data.tasks[c_queue[0]]['execution_time']
                    self._data.resources[resource]['c_task'] = c_queue[0]
                    self._data.tasks[c_queue[0]]['running'] = True
                    self._schedule[c_queue.popleft()] = resource
                    if not c_queue:
                        return self._recurs_sch(p_queue, c_queue)
                        self._down_tick()
                    else:
                        return self._recurs_sch(c_queue, p_queue)
        #if no available resource down tick and try again
        self._down_tick()
        return self._recurs_sch(c_queue, p_queue)
               
                    
    def _check_p_running(self, c_queue):
        '''
        Helper function to check for parent tasks running.
        '''
        if self._data.tasks[c_queue[0]]['parent_tasks']:
            for t in self._data.tasks[c_queue[0]]['parent_tasks']:
                if self._data.tasks[t]['running'] == True:
                    return True
                else:
                    return False
        else:
            return False

  
def main():
    
    args = ArgProcessor(sys.argv[1:])    
    io_yaml_obj = IOYaml()
    tasks, resources=io_yaml_obj.read(args.task_file, args.resource_file)
    
    data = DataPrep(tasks,resources)
    scheduler = Scheduler(data)
    
    schedule = scheduler.gen_schedule()
    
    io_yaml_obj.write(schedule, args.output_file)
    
    
    
if __name__ == '__main__':
    main()