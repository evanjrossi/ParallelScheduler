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
        print os.getcwd()
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
                yaml.dump(ordered_schedule, f)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        
        