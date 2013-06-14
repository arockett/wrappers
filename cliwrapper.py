#!/usr/bin/env python
#
# Created by Aaron Beckett June 13, 2013
# Editted by:
#   Aaron Beckett
#
#
'''Module for graphically managing command line options for a given command.'''

import sys, subprocess
from Wrapper import BasicWrapper
from wrappergui import OptionInputGui

class CLIWrapper(BasicWrapper):
    
    def __init__(self,command='',args=[]):
        # command - what command the user wants to run
        # args  -  a list of tuples of the form: (option name, option representation)
        #          where option representation is something like '-d:' if option takes arg
        #          and something like '-s' if option takes no arg
        # options - a dict where the key is the option name which points to a list
        #           of the form [option name, option representation, option value]
        
        self.base_command = command.strip()
        self.args = [(name.strip(),rep.strip()) for name,rep in args]
        self.options = []
        for arg in self.args:
            self.options.append([arg[0],arg[1],''])
            
        self.build_command()
            
    def preprocess(self):
        self.get_options()
            
    def get_options(self):
        '''Use an OptionInputGui to get all necessary options.'''
        gui = OptionInputGui(self.base_command,self.args,self.options)
        self.base_command,self.args,self.options = gui.result
        
    def build_command(self):
        self.command = ''
        self.command += self.base_command
        for name,arg,value in self.options:
            if value:
                self.command += ' '+arg
            if not isinstance(value,bool):
                self.command += ' '+value
        
    def run_command(self):
        '''Run the command built from the OptionInputGui results.'''
        self.build_command()   
        BasicWrapper.run_command(self)
        
#****** Manage Options ******
            
    def save_options(self):
        pass
    
    def open_options(self):
        pass
    
    def compare_options(self,previous_opts_file):
        pass
            
    

def main(argc,argv):
    '''Open a blank CLIWrapper for editting and automatically run the command it generates.'''
    wrapper = CLIWrapper()
    wrapper.wrap()

if __name__ == '__main__':
    sys.exit(main())
    

