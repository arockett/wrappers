#!/usr/bin/env python
#
# Created by Aaron Beckett June 13, 2013
# Editted by:
#   Aaron Beckett
#
#
'''Gui used by CLIWrapper to get user inputted options.'''

import os
from Tkinter import *
import tkFileDialog

class OptionInputGui:
    
    def __init__(self,command,args,options):
        self.command = command
        self.args = args
        self.options = options
      
        self.root = Tk()
        
        body = Frame(self.root)
        self.body(body)
        body.pack(padx=5,pady=5)
        
        self.root.protocol("WM_DELETE_WINDOW",self.root.destroy)
        
        self.result = self.command, self.args, self.options
        
        self.root.mainloop()
            
#****** Create GUI ******
            
    def body(self,master):
        # Fill Option Frame
        opt_frame = Frame(master)
        for opt in self.options:
            blueprint = self.parse_arg(opt[1])
            if len(blueprint) == 1:
                continue
            elif blueprint[1] == '':
                opt[2] = StringVar()
                self.new_string(opt_frame,opt[0],opt[2])
            elif blueprint[1] == '_file_':
                opt[2] = StringVar()
                try:
                    filetypes = [tuple(ft.split(',')) for ft in blueprint[2:]]
                    self.new_file(opt_frame,opt[0],opt[2],filetypes)
                except IndexError:
                    self.new_file(opt_frame,opt[0],opt[2])
            elif blueprint[1] == '_dir_':
                opt[2] = StringVar()
                self.new_directory(opt_frame,opt[0],opt[2])
            elif blueprint[1] == '_int_':
                continue
            elif blueprint[1] == '_double_':
                continue
            else:
                continue
            opt[1] = blueprint[0]
        opt_frame.pack()
        
        #Make buttonbox
        self.buttonbox(master)
                    
    def parse_arg(self,raw):
        result = raw
        if ':' in result:
            result = result.split(':')
        return result
        
    def new_bool(self,master,name,var):
        pass
                
    def new_string(self,master,name,var):
        box = Frame(master)
        
        label = Label(box, text=name)
        label.pack(padx=5)
        
        entry = Entry(box, width=20, relief=SUNKEN, textvariable=var)
        entry.pack(padx=5,pady=10)
        
        box.pack()
        
    def new_file(self,master,name,var,ext=[('All Types','*')]):
        box = Frame(master)
        
        label = Label(box, text=name)
        label.pack(padx=5)
        
        entry = Entry(box, width=40, relief=SUNKEN, textvariable=var)
        entry.bind("<Button-1>", lambda e: self.select_file(ext,e))
        entry.pack(padx=5,pady=10)
        
        box.pack()
        
    def select_file(self,extensions,event=''):
        path = tkFileDialog.askopenfilename(filetypes=extensions,
                                            initialdir=os.getcwd(),
                                            title='Choose File')
        if path:
            # Account for spaces in the path
            print path
            dirs = path.split('/')
            for i in range(len(dirs)):
                for ch in dirs[i]:
                    if ch.isspace():
                        dirs[i] = '"'+dirs[i]+'"'
            path = '/'.join(dirs)
            print path
            
            event.widget.delete(0,END)
            event.widget.insert(0,path)
            
    def new_directory(self,master,name,var):
        box = Frame(master)
        
        label = Label(box, text=name)
        label.pack(padx=5)
        
        entry = Entry(box, width=40, relief=SUNKEN, textvariable=var)
        entry.bind("<Button-1>", self.select_dir)
        entry.pack(padx=5,pady=10)
        
        box.pack()
        
    def select_dir(self,event=''):
        path = tkFileDialog.askdirectory(initialdir=os.getcwd(),
                                         title='Choose Directory')
        if path:
            # Account for spaces in the path
            print path
            dirs = path.split('/')
            for i in range(len(dirs)):
                for ch in dirs[i]:
                    if ch.isspace():
                        dirs[i] = '"'+dirs[i]+'"'
            path = '/'.join(dirs)
            print path
            
            event.widget.delete(0,END)
            event.widget.insert(0,path)
        
    def new_menu(self,master,name,var,opts=[]):
        pass
        
    def new_int(self,master,name,var):
        pass
        
    def new_double(self,master,name,var):
        pass
            
    def buttonbox(self,master):
        # add standard button box. override if you don't want the
        # standard buttons
        box = Frame(master)

        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=RIGHT, padx=5, pady=5)
        w = Button(box, text="Run", width=10, command=self.run, default=ACTIVE)
        w.pack(side=RIGHT,padx=5, pady=5)

        self.root.bind("&lt;Return>", self.run)
        self.root.bind("&lt;Escape>", self.cancel)

        box.pack()
        
#****** Standar Button Semantics ******
        
    def run(self, event=''):
        # Store entered options and run command with those options
        if not self.validate():
            return
            
        self.root.withdraw()
        self.root.update_idletasks()
        
        self.apply()
        
        self.root.quit()
        
    def cancel(self, event=''):
        # Close window
        self.result = None
        self.root.quit()
        
    def validate(self):
        return 1
        
    def apply(self):
        for opt in self.options:
            opt[2] = opt[2].get()
            if not isinstance(opt[2],bool):
                opt[2] = str(opt[2])
            
        self.result = self.command, self.args, self.options
            

