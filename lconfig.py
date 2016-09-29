#!/usr/share/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

class ConfDialog(QtGui.QMessageBox):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        
        metaDataKeys = ['FOV', 'Start Voltage', 'Sample Temp.', 'Main',
                        'timestamp', 'test']
        
        # Instantiate UI elements
        innerLayoutCheckboxes = QtGui.QGridLayout()
        
        ii = 0
        for item in metaDataKeys:
            ## Use list with strings to create checkboxes
            innerLayoutCheckboxes.addWidget(QtWidgets.QCheckBox(item), ii-ii%2,ii%2)
            ii += 1

        self.layout().addLayout(innerLayoutCheckboxes, 0, 0)
        
        self.setStandardButtons(self.Ok | self.Cancel)
        #self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Configuration')
        
        
        
