from PyQt5 import QtCore, QtGui, QtWidgets

class ConfDialog(QtGui.QMessageBox):
    def __init__(self, currentKeys, parent=None):
        QtGui.QDialog.__init__(self, parent)
        
        _availMetaDataKeys = ('FOV', 'Start Voltage', 'Sample Temp.',
                             'Main', 'timestamp', 'Dimension', 'id', 'size',
                             'version', 'Camera Exposure', 'Average Images', 
                             'Mitutoyo X', 'Mitutoyo Y')
        self._metaDataBoxes = dict()

        # Instantiate UI elements
        layoutCheckboxes = QtGui.QGridLayout()
        ii = 0
        for item in _availMetaDataKeys:
            ## Use list with strings to create checkboxes
            self._metaDataBoxes[item] = QtWidgets.QCheckBox(item)
            layoutCheckboxes.addWidget(self._metaDataBoxes[item], ii-ii%3,ii%3)
            ii += 1

        self.layout().addLayout(layoutCheckboxes, 0, 0)
        self.setStandardButtons(self.Ok | self.Cancel)
        self.setWindowTitle('Configuration')
        self.setMetaDataKeys(currentKeys)
        
    def getMetaDataKeys(self):
        dispKeys = []
        for key in self._metaDataBoxes:
            if self._metaDataBoxes[key].isChecked():
                dispKeys.append(key)
        return dispKeys

    def setMetaDataKeys(self, dispedKeys):
        for key in dispedKeys:
            self._metaDataBoxes[key].setChecked(True)
