#!/usr/bin/env python
#
# Created by Aaron Beckett June 13, 2013
# Editted by:
#   Aaron Beckett
#
#
'''Module for graphically managing command line options for a given command.'''

import sys

class CLIWrapper:
    
    def __init__(self,command,args=[]):
        # command - what command the user wants to run
        # args  -  a list of tuples of the form: (option name, option representation)
        #          where option representation is something like '-d:' if option takes arg
        #          and something like '-s' if option takes no arg
        # options - a dict where the key is the option name which points to a list
        #           of the form [option representation, option value]
        self.command = command
        self.args = args
        self.options = []
        for arg in args:
            self.options.append([arg[0],arg[1],''])
        
#****** Manage Options ******
            
    def save_options(self):
        pass
    
    def open_options(self):
        pass
    
    def compare_options(self,previous_opts_file):
        pass
            
    

def main(argc,argv):
    pass

if __name__ == '__main__':
    argc = len(sys.argv)
    sys.exit(main(argc,sys.argv))
    

