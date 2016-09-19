#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

class lMetaDataModel(QtCore.QAbstractListModel):
    """Class constructing the view model for the meta data"""
    def __init__(self, metadata={}, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__metadata = metadata
        # Define which data to display
        # TODO Should be configuralbe
        self.__dispedKeys = ('FOV', 'Start Voltage', 'Sample Temp.',
                             'Main', 'timestamp')  

    def rowCount(self, parent):
        return len(self.__dispedKeys)+1

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            if index.row() < len(self.__dispedKeys):
                row = index.row()
                key = self.__dispedKeys[row]
                value = self.__metadata[key]
                key, value = self.format_metadata(key, value)
                ## TODO Fix intendention
                return '{:<13}\t {}'.format(key, value)
            else:
                return '{0:<13}  {1} x {2} px'.format('Dimension',
                self.__metadata['width'], self.__metadata['height'])

    def format_metadata(self, key, value):
        if key == 'timestamp':
            key = 'Measured'
        if key == 'Main' or key == 'Column':
            value = '{0:.1e} {1}'.format(value[0], value[1])
        elif type(value) is list:
            value = '{0:.1f} {1}'.format(value[0], value[1])
        return key, value
 
