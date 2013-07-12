#!/usr/bin/env python
#
# Created by Aaron Beckett July 9, 2013
# Editted by:
#   Aaron Beckett
#
#
'''Chamview Gui used by CLIWrapper to get user inputted options for Chamview.'''

from PyQt4.QtGui import *
from PyQt4.QtCore import SIGNAL, SLOT

class CollapsibleFrame( QWidget ):

    def __init__(self, toggle_widget, parent=None):
        QWidget.__init__(self, parent)
        self.__setup()
        self.connect(toggle_widget, SIGNAL("toggled(bool)"),
                     self.frame, SLOT("setVisible(bool)"))

    def __setup(self):
        layout = QVBoxLayout()
        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        self.frame.hide()
        layout.addWidget(self.frame)
        QWidget.setLayout(self, layout)

    def setLayout(self, layout):
        self.frame.setLayout(layout)

class WindowStream(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self,parent)
        layout = QVBoxLayout()

        self.setWindowTitle('Grab Frames')
        self.textedit = QTextEdit()
        layout.addWidget(self.textedit)

        self.setLayout(layout)

    def write(self, text):
        self.textedit.append(text)

