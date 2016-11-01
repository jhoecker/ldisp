# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets

class lMetaDataModel(QtCore.QAbstractListModel):
    """Class constructing the view model for the meta data"""
    def __init__(self, dispedData, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self._metadata = dispedData

    def rowCount(self, parent):
        return len(self._metadata)

    def data(self, index, role):
        data_keys = list(self._metadata.keys())
        if role == QtCore.Qt.DisplayRole:
            if index.row() < len(self._metadata):
                row = index.row()
                key = data_keys[row]
                value = self._metadata[key]
                key, value = self.format_metadata(key, value)
                ## TODO Fix intendention
                return '{:<13} {}'.format(key, value)

    def format_metadata(self, key, value):
        if key == 'timestamp':
            key = 'Measured'
            value = value.strftime("%Y-%m-%d %H:%M:%S")
        if key == 'Main' or key == 'Column':
            value = '{0:.1e} {1}'.format(value[0], value[1])
        elif type(value) is list:
            try:
                value = '{0:.1f} {1}'.format(value[0], value[1])
            except ValueError:
                value = '{0} {1}'.format(value[0], value[1])
        return key, value
    

class MetaData(object):
    """Manages the metadata and its keys that are stored in every LEEM image.
    Own class since the Keys should not change every time a new model is 
    loaded."""
    ## Use class variable for currentKeys and change only on demand
    ## Then the Keys are not set to default if a new object is generated
    currentKeys = ('FOV', 'Start Voltage', 'Sample Temp.',
                   'Main', 'Dimension')
    def __init__(self, metadata={}, dispKeys=None):
        self._metadata = metadata

    @staticmethod
    def setCurrentKeys(newKeys):
        MetaData.currentKeys = newKeys

    def getDispedData(self):
        _dispData = dict()
        for item in MetaData.currentKeys:
            if item in self._metadata.keys():
                _dispData[item] = self._metadata[item]
            elif item == 'Dimension':
                _dispData[item] ='{0} x {1} px'.format(self._metadata['width'],
                                                       self._metadata['height'])
        return _dispData
