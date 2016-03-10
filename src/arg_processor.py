'''
Created on Mar 6, 2016

@author: Evan
'''
import sys
import os
import getopt

class ArgProcessor(object):
    '''
    A class to encapsulate passing args to the application
    '''

    def __init__(self, argv):
        '''
        Constructor
        '''
        self.task_file = ''
        self.resource_file = '' 
        self.output_file = ''
        self.usage = 'Usage:\n-t <tasks.yaml> \n-r <resources.yaml> \n-o <output.yaml>'
        self.process_args(argv)
          
    def check_yaml(self, filepath):
        
        if filepath[-4:].lower().strip("'") != "yaml": 
            raise ValueError('File type must be yaml')
            print self.usage
            sys.exit(1)
            
        else:
            return filepath
        
        #os.path.exists(path)
    def process_args(self,argv):
        
        try:
            options, args = getopt.getopt(argv,'ht:r:o:',['tasks=','resources=','output='])
        except getopt.GetoptError as err:
        # print help information and exit:
            print err 
            print self.usage
            sys.exit(2)
        if not options:
            print self.usage
            sys.exit(1)
        for o, a in options:
            if o == '-h':
                print self.usage
                sys.exit()
            elif o in ('-t', '--tasks'):
                self.task_file = self.check_yaml(a)
            elif o in ('-r', '--resources'):
                self.resource_file = self.check_yaml(a)
            elif o in ('-o', '--output'):
                self.output_file = a