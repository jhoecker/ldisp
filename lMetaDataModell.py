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
        _dispedKeys = ('FOV', 'Start Voltage', 'Sample Temp.',
                             'Main', 'timestamp', 'test')
        self._dispData = dict()
        self.getDispedValues(_dispedKeys)

    def rowCount(self, parent):
        return len(self._dispData)+1

    def data(self, index, role):
        data_keys = list(self._dispData)
        if role == QtCore.Qt.DisplayRole:
            if index.row() < len(self._dispData):
                row = index.row()
                key = data_keys[row]
                value = self.__metadata[key]
                key, value = self.format_metadata(key, value)
                return '{0}: {1}'.format(key, value)
            else:
                return '{0}:  {1} x {2} px'.format('Dimension',
                self.__metadata['width'], self.__metadata['height'])

    def format_metadata(self, key, value):
        if key == 'timestamp':
            key = 'Measured'
        if key == 'Main' or key == 'Column':
            value = '{0:.1e} {1}'.format(value[0], value[1])
        elif type(value) is list:
            value = '{0:.1f} {1}'.format(value[0], value[1])
        return key, value
    
    def getDispedValues(self, _dispKeys):
        """Check that the metadata which should be displayed in the metaDataView
        is available"""
        for item in _dispKeys:
            if item in self.__metadata.keys():
                self._dispData[item] = self.__metadata[item]
        
 
