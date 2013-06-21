#!/usr/bin/env python
#
# Created by Aaron Beckett June 13, 2013
# Editted by:
#   Aaron Beckett
#
#
'''Gui used by CLIWrapper to get user inputted options.'''

import os,sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class OptionInputGui:
	def __init__(self, command, args, options, cliargs):
		app = QApplication(cliargs)
		win = OptionInputWindow(command,args,options)
		win.show()
		app.connect(app, SIGNAL("lastWindowClosed()"),
					app, SLOT("quit()"))
		app.exec_()
		self.result = win.result

class OptionInputWindow(QMainWindow):
    
	def __init__(self, command, args, options, *extra):
		self.command = QString(command)
		self.args = args
		self.options = options
		apply(QWidget.__init__, (self, ) + extra)

		widget = QWidget()
		layout = QVBoxLayout()
		self.fill(layout)
		widget.setLayout(layout)
		widget.setWindowTitle("Parameter Manager")
		self.setCentralWidget(widget)
        
		self.result = self.command, self.args, self.options
        
#****** Create GUI ******

	def fill(self,body):
		# Create widget for the command
		body.addWidget(QLabel('Command'))
		command_edit = self.new_string(self.command)
		command_edit.setText(self.command)
		command_edit.selectAll()
		body.addWidget(command_edit)
		
		# Horizontal line
		hline = QFrame()
		hline.setFrameStyle( QFrame.HLine | QFrame.Raised )
		hline.setLineWidth(2)
		hline.setMidLineWidth(2)
		body.addWidget(hline)
		
        # Create widgets for each option
		for opt in self.options:
			blueprint = self.parse_arg(opt[1])
			print blueprint
			if len(blueprint) == 1:
				opt[2] = False
				body.addWidget(self.new_bool(opt))
			elif blueprint[1] == '':
				body.addWidget(QLabel(opt[0]))
				opt[2] = QString('')
				body.addWidget(self.new_string(opt))
			elif blueprint[1] == '_file_':
				body.addWidget(QLabel(opt[0]))
				opt[2] = QString('')
				try:
					filetypes = [tuple(ft.split(',')) for ft in blueprint[2:]]
					filetype_str = ''
					for typ in filetypes:
						filetype_str += typ[0]+' ('
						for ext in typ[1:]:
							filetype_str += ext + ' '
						filetype_str = filetype_str[:-1] + ')'
						filetype_str += ';;'
					filetype_str = filetype_str[:-2]
					body.addLayout(self.new_file(opt,filetype_str))
				except IndexError:
					body.addLayout(self.new_file(opt))
			elif blueprint[1] == '_dir_':
				body.addWidget(QLabel(opt[0]))
				opt[2] = QString()
				body.addLayout(self.new_directory(opt))
			elif blueprint[1] == '_int_':
				box = QHBoxLayout()
				box.addWidget(QLabel(opt[0]))
				try:
					min,max = blueprint[2],blueprint[3]
					box.addWidget(self.new_int(opt,min,max))
				except IndexError:
					box.addWidget(self.new_int(opt))
				body.addLayout(box)
			elif blueprint[1] == '_double_':
				box = QHBoxLayout()
				box.addWidget(QLabel(opt[0]))
				try:
					min,max = blueprint[2],blueprint[3]
					box.addWidget(self.new_double(opt,min,max))
				except IndexError:
					box.addWidget(self.new_double(opt))
				body.addLayout(box)
			else:
				continue
			opt[1] = blueprint[0]
        
		# Horizontal line
		hline = QFrame()
		hline.setFrameStyle( QFrame.HLine | QFrame.Raised )
		hline.setLineWidth(3)
		hline.setMidLineWidth(3)
		body.addWidget(hline)
        
		#Make buttonbox
		body.addLayout(self.buttonbox())
        
	def parse_arg(self,raw):
		result = raw
		if ':' in result:
			result = result.split(':')
		else:
			result = [result]
		return result
		
	def store_value(self,index,value):
		print value
		print type(value)
		if isinstance(value, QString):
			self.options[index][2].swap(value)
		else:
			self.options[index][2] = value
        
	def new_bool(self,o):
		checkbox = QCheckBox(o[0])
		func = lambda: self.store_value(self.options.index(o),checkbox.isChecked())
		self.connect(checkbox,SIGNAL("stateChanged(int)"), func)
		return checkbox
                
	def new_string(self,o):
		qedit = QLineEdit('')
		if not isinstance(o,QString):
			func = lambda: self.store_value(self.options.index(o),qedit.text())
		else:
			func = lambda s=qedit.text(): self.command.swap(s)
		self.connect(qedit,SIGNAL("textChanged(QString)"), func)
		return qedit
        
	def new_file(self,o,ext='All Types (*)'):
		box = QHBoxLayout()
		
		qedit = QLineEdit('')
		func = lambda: self.store_value(self.option.index(o),qedit.text())
		self.connect(qedit,SIGNAL("textChanged(QString)"), func)
		browse = QPushButton('Browse')
		browse.clicked.connect(lambda: self.select_file(qedit,ext))
		
		box.addWidget(qedit)
		#box.addSeparator(2)
		box.addWidget(browse)
		return box
        
	def select_file(self,ledit,extensions):
		path = QFileDialog.getOpenFileName(None,QString("Select File"),
												QString(os.getcwd()),
												QString(extensions))	
		if path:
            # Account for spaces in the path
			dirs = path.split('/')
			for i in range(len(dirs)):
				for ch in dirs[i]:
					if ch.isspace():
						dirs[i] = '"'+dirs[i]+'"'
			path = '/'.join(dirs)
            
			ledit.setText(path)
            
	def new_directory(self,o):
		box = QHBoxLayout()
		
		qedit = QLineEdit('')
		func = lambda: self.store_value(self.option.index(o),qedit.text())
		self.connect(qedit,SIGNAL("textChanged(QString)"), func)
		browse = QPushButton('Browse')
		browse.clicked.connect(lambda: self.select_dir(qedit))
		
		box.addWidget(qedit)
		#box.addSeparator(2)
		box.addWidget(browse)
		
		return box
        
	def select_dir(self,ledit):
		path = QFileDialog.getExistingDirectory(None,QString('Select Directory'),
													 QString(os.getcwd()),
													 QFileDialog.ShowDirsOnly)
		if path:
            # Account for spaces in the path
			dirs = path.split('/')
			for i in range(len(dirs)):
				for ch in dirs[i]:
					if ch.isspace():
						dirs[i] = '"'+dirs[i]+'"'
			path = '/'.join(dirs)
			
			ledit.setText(path)
			
	def new_int(self,o,min=None,max=None):
		intspin = QSpinBox()
		if min:
			intspin.setMinimum(int(min))
		if max:
			intspin.setMaximum(int(max))
		func = lambda: self.store_value(self.option.index(o),intspin.value())
		self.connect(intspin, SIGNAL("valueChanged()"), func)
		return intspin
		
        
	def new_double(self,o,min=None,max=None):
		doublespin = QDoubleSpinBox()
		if min:
			doublespin.setMinimum(float(min))
		if max:
			doublespin.setMaximum(float(max))
		func = lambda: self.store_value(self.option.index(o),doublespin.value())
		self.connect(doublespin, SIGNAL("valueChanged()"), func)
		return doublespin
        
	def new_menu(self,o,opts=[]):
		pass
            
	def buttonbox(self):
		box = QHBoxLayout()
		
		save_button = QPushButton('Save')
		save_button.clicked.connect(self.save)
		run_button = QPushButton('Run')
		run_button.clicked.connect(self.run)
		
		box.addWidget(save_button)
		box.addStretch()
		box.addWidget(run_button)
		
		return box
        
#****** Standard Button Semantics ******

	def save(self):
		print 'save'
        
	def run(self, event=''):
        # Store entered options and run command with those options
		if not self.validate():
			return
        
		self.apply()
        
	def cancel(self, event=''):
        # Close window
		self.result = None
        
	def validate(self):
		return 1
        
	def apply(self):
		opts = []
		for opt in self.options:
			opts.append([opt[0],opt[1],str(opt[2])])
		print self.command
		print self.args
		print opts
		self.result = str(self.command), self.args, opts	


