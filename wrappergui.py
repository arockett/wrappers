#!/usr/bin/env python
#
# Created by Aaron Beckett June 13, 2013
# Editted by:
#   Aaron Beckett
#
#
'''Module for graphically managing command line options for a given command.'''

from Tkinter import *

class Gui:
    
    def __init__(self,command,args,options):
        self.command = command
        self.args = args
        self.options = options
    
    def get_options(self):   
        self.root = Tk()
        
        body = Frame(self.root)
        self.body(body)
        body.pack(padx=5,pady=5)
        
        self.root.protocol("WM_DELETE_WINDOW",self.cancel)
        
        self.result = self.options
        
        self.root.mainloop()
            
#****** Create GUI ******
            
    def body(self,master):
        pass
        
    def new_string(self):
        pass
        
    def new_path(self):
        pass
        
    def new_menu(self):
        pass
        
    def new_int(self):
        pass
        
    def new_double(self):
        pass
            
    def buttonbox(self):
        pass
        
#****** Apply Selected Options ******
        
    def run(self, event=''):
        # Store entered options and run command with those options
        if not self.validate():
            return
            
        self.root.withdraw()
        self.root.update_idletasks()
        
        self.apply()
        
        self.run_command()
        
        self.cancel()
        
    def cancel(self, event=''):
        # Close window
        self.root.quit()
        
    def validate(self):
        return 1
        
    def apply(self):
        pass
            
    def run_command(self):
        pass