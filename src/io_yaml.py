'''
Created on Mar 6, 2016

@author: Evan
'''
import yaml
import os

class IOYaml(object):
    '''
    A singleton class that reads and writes .yaml files
    '''
    __instance = None
    def __new__(cls):
        if IOYaml.__instance is None:
            IOYaml.__instance = object.__new__(cls)
        return IOYaml.__instance

        
    def read(self, tasks, resources):
        try:
        
            with open(tasks) as t:
                l_tasks = yaml.load(t)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            
        try:    
            with open(resources) as r:
                l_resources = yaml.load(r)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        
        return l_tasks, l_resources
    
    def write(self, ordered_schedule, file_name):
        
        try:
            with open(file_name, 'w') as f:
                for k in ordered_schedule:
                    print k,': ',ordered_schedule[k]
                    f.write('{0}: {1}\n'.format(k, ordered_schedule[k]))
                    
                print '\noutput file located at', os.path.abspath(file_name)
            
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            

            
            
            
            
        
        