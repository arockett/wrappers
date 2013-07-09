#!/usr/bin/env python
#
# Created by Aaron Beckett June 13, 2013
# Editted by:
#   Aaron Beckett
#
#
'''Module for graphically managing command line options for a given command.'''

import os, sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Wrapper import BasicWrapper
from cligui import OptionInputWindow

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
            self.options.append([arg[0],arg[1].split(':')[0],''])

        self.build_command()

    def preprocess(self):
        self.get_options()

    def get_options(self):
        '''Use an OptionInputGui to get all necessary options.'''

        app = QApplication(sys.argv)
        app.connect(app, SIGNAL("lastWindowClosed()"),
                    app, SLOT("quit()"))
        self.win = self.create_window()

        def run():
            if self.isvalid(self.win.result):
                self.base_command, self.args, self.options = self.win.result
                self.run_command(self.base_command, self.options)
            else:
                print 'bad options'

        app.connect(self.win, SIGNAL("readyToRun()"), run)
        save = lambda (cm,arg,op)=self.win.result: self.save_options(cm,arg,op)
        app.connect(self.win, SIGNAL("readyToSave()"), save)

        self.win.show()
        app.exec_()

        sys.exit(0)

    def create_window(self):
        return OptionInputWindow(self.base_command, self.args, self.options)

    def run_command(self,cmd,opts):
        '''Run the command built from the OptionInputGui results.'''
        self.build_command(cmd,opts)
        print self.command
        BasicWrapper.run_command(self)

    def build_command(self,cmd=None,opts=None):
        if not cmd: cmd = self.base_command
        if not opts: opts = self.options
        self.command = ''
        self.command += cmd
        for name,arg,value in opts:
            if value:
                self.command += ' '+arg
                if not isinstance(value,bool):
                    self.command += ' '+value

    def isvalid(self,result):
        return True

#****** Manage Options ******

    def save_options(self,cmd,args,opts):
        print 'SAVE'
        print cmd
        print args
        print opts

    def open_options(self,previous_opts_file):
        pass

    def compare_options(self,previous_opts_file):
        pass



def main():
    '''Open a blank CLIWrapper for editting and automatically run the command it generates.'''
    os.chdir('../chamview')
    wrapper = CLIWrapper(command='jibber-jabber',
                         args=[('String','-l:'),
                               ('No option, just value',':'),
                               ('File','-o:_file_:Text File,*.txt'),
                               ('Directory','-d:_dir_|*'),
                               ('Boolean','-s|*'),
                               ('Int','-i:_int_'),
                               ('Int min/max','-I:_int_:0:19'),
                               ('Float','-f:_float_'),
                               ('Float min/max','-F:_float_:2.5:4.5'),
                               ('Menu','-m:_menu_:One:Two:Three')])
    wrapper.wrap()

if __name__ == '__main__':
    sys.exit(main())


