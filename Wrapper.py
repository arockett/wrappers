#
# Created by Aaron Beckett June 13, 2013
# Editted by:
#   Aaron Beckett
#
#
'''General structure for wrapper objects.'''

import subprocess


class BasicWrapper:
    
    def __init__(self,command=''):
        '''Create a Wrapper object by passing the command that runs a program
        the Wrapper can wrap around.
        '''
        self.command = command.strip()
    
    def preprocess(self):
        '''This is were the Wrapper does all of its work prior to passing 
        control to the program it wraps around.
        '''
        return      # override this method
        
    def run_command(self):
        '''Run the main program after doing preprocessing work.
        '''
        subprocess.call(self.command.split())
        
    def wrap(self):
        '''Make the Wrapper go through the sequence of its preprocessing activities
        then run the main program.
        '''
        self.preprocess()
        self.run_command()
